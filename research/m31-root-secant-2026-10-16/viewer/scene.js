import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';

// Rendering only: positions/quaternions and error arrays are supplied by verified records.
export function createScene(host) {
  const renderer = new THREE.WebGLRenderer({antialias: true, alpha: false});
  renderer.setPixelRatio(Math.min(globalThis.devicePixelRatio || 1, 2));
  renderer.setClearColor('#102431');
  host.append(renderer.domElement);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, 1, 0.01, 3000);
  camera.up.set(0, 0, 1);
  const orbit = new OrbitControls(camera, renderer.domElement);
  orbit.enableDamping = false;
  scene.add(new THREE.HemisphereLight(0xd5f5ff, 0x325149, 3));
  const light = new THREE.DirectionalLight(0xffffff, 2);
  light.position.set(10, -20, 50);
  scene.add(light);
  let group = new THREE.Group();
  scene.add(group);
  let events = null, n = 0, body = null, rotors = null, labels = [], frameIndex = 0, scale = 4;
  let savedErrors = null, metric = 'rotor', invalidRoots = [], initializer = true;
  let center = new THREE.Vector3(), radius = 1;
  const obj = new THREE.Object3D(), position = new THREE.Vector3(), quaternion = new THREE.Quaternion(), offset = new THREE.Vector3();
  const corners = [[0.028, 0.028, 0], [-0.028, 0.028, 0], [-0.028, -0.028, 0], [0.028, -0.028, 0]];
  const low = new THREE.Color('#50c7d8'), limit = new THREE.Color('#edbd57'), high = new THREE.Color('#e66048');
  const invalidColor = new THREE.Color('#f052bb'), missingColor = new THREE.Color('#8a98a2'), color = new THREE.Color();
  const render = () => renderer.render(scene, camera);
  orbit.addEventListener('change', render);

  function shade(value, invalid) {
    if (invalid) return color.copy(invalidColor);
    if (value === null || value === undefined || !Number.isFinite(value)) return color.copy(missingColor);
    const ratio = Math.max(0, value / 0.001);
    return ratio <= 1 ? color.copy(low).lerp(limit, ratio) : color.copy(limit).lerp(high, Math.min(1, (ratio - 1) / 4));
  }
  function reset() {
    const vertical = THREE.MathUtils.degToRad(camera.fov) / 2;
    const horizontal = Math.atan(Math.tan(vertical) * camera.aspect);
    const distance = 1.18 * radius / Math.sin(Math.min(vertical, horizontal));
    camera.position.copy(center).add(new THREE.Vector3(1, -1.6, 1).normalize().multiplyScalar(distance));
    orbit.target.copy(center);
    orbit.minDistance = Math.max(0.15, radius * 0.1);
    orbit.maxDistance = Math.max(15, radius * 12);
    orbit.update();
    render();
  }
  function frame(index, errors = savedErrors, channel = metric, invalids = invalidRoots, isInitializer = initializer) {
    if (!events) return;
    frameIndex = index; savedErrors = errors; metric = channel; invalidRoots = invalids; initializer = isInitializer;
    const states = events[index].states;
    const invalidByDrone = Array.from({length: n}, () => new Set());
    for (const value of invalids) invalidByDrone[value.drone].add(value.rotor);
    for (let i = 0; i < n; i++) {
      // No pose interpolation or quaternion normalization: retain the source numbers.
      position.fromArray(states[i], 0);
      quaternion.fromArray(states[i], 6);
      obj.position.copy(position); obj.quaternion.copy(quaternion); obj.scale.setScalar(scale); obj.updateMatrix();
      body.setMatrixAt(i, obj.matrix);
      const values = initializer || !errors ? null : channel === 'rotor' ? errors.rotor[i] : errors[channel][i];
      const bodyValue = Array.isArray(values) ? Math.max(...values) : values;
      body.setColorAt(i, shade(bodyValue, invalidByDrone[i].size > 0));
      for (let r = 0; r < 4; r++) {
        offset.fromArray(corners[r]).multiplyScalar(scale).applyQuaternion(quaternion);
        obj.position.copy(position).add(offset); obj.updateMatrix();
        rotors.setMatrixAt(4 * i + r, obj.matrix);
        const value = Array.isArray(values) ? values[r] : values;
        rotors.setColorAt(4 * i + r, shade(value, invalidByDrone[i].has(r)));
      }
      labels[i].position.copy(position).add(new THREE.Vector3(0, 0, 0.08 * scale));
      labels[i].scale.set(0.07 * scale, 0.045 * scale, 1);
    }
    body.instanceMatrix.needsUpdate = true;
    rotors.instanceMatrix.needsUpdate = true;
    body.instanceColor.needsUpdate = true;
    rotors.instanceColor.needsUpdate = true;
    host.dataset.frame = String(index);
    host.dataset.size = String(scale);
    host.dataset.metric = channel;
    host.dataset.invalidRotors = String(invalids.length);
    render();
  }
  function makeLabel(id) {
    const canvas = document.createElement('canvas');
    canvas.width = 112; canvas.height = 72;
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Drone label rendering unavailable');
    ctx.fillStyle = 'rgba(7,24,34,0.86)';
    ctx.fillRect(5, 7, 102, 58);
    ctx.font = '500 42px system-ui, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillStyle = '#e2f0f3'; ctx.fillText(String(id), 56, 38);
    const texture = new THREE.CanvasTexture(canvas);
    const label = new THREE.Sprite(new THREE.SpriteMaterial({map: texture, transparent: true, depthTest: false, depthWrite: false}));
    label.renderOrder = 3;
    return label;
  }
  function load(sourceEvents, count) {
    events = sourceEvents; n = count;
    scene.remove(group);
    group.traverse(object => { object.geometry?.dispose(); object.material?.map?.dispose(); object.material?.dispose(); });
    group = new THREE.Group(); scene.add(group);
    const bounds = new THREE.Box3();
    for (const event of events) for (const state of event.states) bounds.expandByPoint(position.fromArray(state, 0));
    center = bounds.getCenter(new THREE.Vector3());
    radius = bounds.getSize(new THREE.Vector3()).length() / 2 + 0.8;
    const span = Math.max(bounds.max.x - bounds.min.x, bounds.max.y - bounds.min.y, 2);
    const grid = new THREE.GridHelper(span * 1.2, 20, 0x47717d, 0x25404d);
    grid.rotation.x = Math.PI / 2;
    grid.position.set(center.x, center.y, bounds.min.z - 0.25);
    group.add(grid);
    const material = new THREE.MeshStandardMaterial({color: 0xffffff, roughness: 0.7});
    body = new THREE.InstancedMesh(new THREE.BoxGeometry(0.034, 0.044, 0.015), material, n);
    rotors = new THREE.InstancedMesh(new THREE.TorusGeometry(0.023, 0.0035, 5, 14), material, 4 * n);
    body.frustumCulled = false; rotors.frustumCulled = false;
    group.add(body, rotors);
    labels = Array.from({length: n}, (_, id) => makeLabel(id));
    group.add(...labels);
    host.dataset.instances = String(n);
    host.dataset.frames = String(events.length);
    frame(0, null, 'rotor', [], true);
    resize();
    reset();
  }
  function size(value) {
    if (![1, 4, 8].includes(value)) return;
    scale = value;
    frame(frameIndex);
  }
  function resize() {
    const rect = host.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    renderer.setSize(rect.width, rect.height, false);
    camera.aspect = rect.width / rect.height;
    camera.updateProjectionMatrix();
    if (events) reset(); else render();
  }
  new ResizeObserver(resize).observe(host);
  renderer.domElement.addEventListener('webglcontextlost', event => { event.preventDefault(); host.dispatchEvent(new CustomEvent('scene-failure', {detail: 'WebGL context lost. Reload to reverify evidence.'})); });
  // Read-only rendered-matrix inspection supports reproducible visual QA.
  host.__inspect = () => ({n, frameIndex, scale,
    matrices: body ? Array.from(body.instanceMatrix.array) : [],
    rotorMatrices: rotors ? Array.from(rotors.instanceMatrix.array) : [],
    bodyColors: body?.instanceColor ? Array.from(body.instanceColor.array) : [],
    camera: camera.position.toArray()});
  return {load, frame, size, reset};
}
