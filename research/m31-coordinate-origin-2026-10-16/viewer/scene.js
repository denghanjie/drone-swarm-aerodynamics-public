import * as T from '../../../outputs/step02b-source/vendor/three.module.js';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
import {N} from './evidence.js';

// These transforms draw saved poses/offsets only. No scientific geometry is rebuilt.
export function createScene(host, initialFrame, onSource) {
  host.replaceChildren();
  const scene = new T.Scene(), cloud = new T.Group(), markers = new T.Group(), links = new T.Group();
  scene.background = new T.Color('#102031'); scene.add(cloud, markers, links);
  const camera = new T.PerspectiveCamera(45, 1, .01, 2000); camera.up.set(0, 0, 1);
  const renderer = new T.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); host.append(renderer.domElement);
  const orbit = new OrbitControls(camera, renderer.domElement); orbit.enableDamping = false;
  scene.add(new T.HemisphereLight(0xffffff, 0x536075, 3));
  const light = new T.DirectionalLight(0xffffff, 2); light.position.set(5, -10, 30); scene.add(light);
  const body = new T.InstancedMesh(new T.BoxGeometry(.045, .032, .018), new T.MeshStandardMaterial(), N);
  const arms = new T.InstancedMesh(new T.BoxGeometry(.095, .008, .007), new T.MeshStandardMaterial(), N * 2);
  body.frustumCulled = arms.frustumCulled = false; cloud.add(body, arms);
  const position = new T.Vector3(), quaternion = new T.Quaternion(), matrix = new T.Matrix4(), scale = new T.Vector3(3, 3, 3), hiddenScale = new T.Vector3(0, 0, 0);
  const box = new T.Box3(), shift = new T.Vector3();
  let frame, bodyMatrices, armMatrices, mode = 'whole', selectedReceiver = initialFrame.receiverIds[0], selectedSource = 0, receiverPoint, contributorIDs = [], lastShow, disposed = false;
  const point = id => new T.Vector3(frame.poses[id * 17], frame.poses[id * 17 + 1], frame.poses[id * 17 + 2]).sub(shift);
  const render = () => {if (!disposed) renderer.render(scene, camera);};
  const clear = group => {for (const child of [...group.children]) {child.geometry?.dispose();child.material?.dispose();group.remove(child);}};
  function visibility() {
    const visible = new Set([...contributorIDs, selectedReceiver, selectedSource]);
    for (let id = 0; id < N; id++) {
      const hidden = mode === 'focused' && !visible.has(id);
      matrix.fromArray(bodyMatrices, id * 16); if (hidden) matrix.scale(hiddenScale); body.setMatrixAt(id, matrix);
      for (let arm = 0; arm < 2; arm++) {const index = 2 * id + arm;matrix.fromArray(armMatrices, index * 16);if (hidden) matrix.scale(hiddenScale);arms.setMatrixAt(index, matrix);}
    }
    body.instanceMatrix.needsUpdate = arms.instanceMatrix.needsUpdate = true;
    document.body.dataset.visibleBodies = String(mode === 'focused' ? visible.size : N);
  }
  function fit(next = mode) {
    mode = next; if (lastShow) show(lastShow); else visibility();
    const bounds = mode === 'whole' ? box.clone() : new T.Box3().expandByPoint(point(selectedReceiver)).expandByPoint(receiverPoint).expandByPoint(point(selectedSource));
    if (mode === 'focused') for (const id of contributorIDs) bounds.expandByPoint(point(id));
    const center = bounds.getCenter(new T.Vector3()), radius = Math.max(.8, bounds.getSize(new T.Vector3()).length() / 2);
    const vertical = T.MathUtils.degToRad(camera.fov / 2), half = Math.min(vertical, Math.atan(Math.tan(vertical) * camera.aspect));
    camera.position.copy(center).add(new T.Vector3(.8, -1, .7).normalize().multiplyScalar(1.15 * radius / Math.sin(half)));
    orbit.target.copy(center); orbit.update(); document.body.dataset.view = mode; render();
  }
  function sphere(at, radius, tint, order) {
    const mesh = new T.Mesh(new T.SphereGeometry(radius, 12, 8), new T.MeshBasicMaterial({color: tint, depthTest: false}));
    mesh.position.copy(at); mesh.renderOrder = order; markers.add(mesh);
  }
  function show(state) {
    lastShow = state;
    const {colors, receiver, source, offset, positiveIDs, showLinks} = state;
    selectedReceiver = receiver; selectedSource = source; contributorIDs = positiveIDs;
    receiverPoint = point(receiver);
    if (offset) receiverPoint.add(new T.Vector3(...offset));
    const color = new T.Color();
    for (let id = 0; id < N; id++) {
      color.setRGB(colors[3 * id], colors[3 * id + 1], colors[3 * id + 2]);
      body.setColorAt(id, color); arms.setColorAt(2 * id, color); arms.setColorAt(2 * id + 1, color);
    }
    body.instanceColor.needsUpdate = arms.instanceColor.needsUpdate = true;
    clear(markers); clear(links);
    for (const id of frame.receiverIds) if (mode === 'whole' || id === receiver || id === source || positiveIDs.includes(id)) sphere(point(id), id === receiver ? .07 : .045, id === receiver ? '#62dfec' : '#5ba8a8', 25);
    sphere(point(source), .055, '#ffffff', 27);
    if (offset) sphere(receiverPoint, .026, '#62dfec', 28);
    if (showLinks && positiveIDs.length) {
      const points = [], vertexColors = [];
      for (const id of positiveIDs) {
        points.push(...point(id).toArray(), ...receiverPoint.toArray());
        for (let end = 0; end < 2; end++) vertexColors.push(colors[3 * id], colors[3 * id + 1], colors[3 * id + 2]);
      }
      const geometry = new T.BufferGeometry(); geometry.setAttribute('position', new T.Float32BufferAttribute(points, 3)); geometry.setAttribute('color', new T.Float32BufferAttribute(vertexColors, 3));
      links.add(new T.LineSegments(geometry, new T.LineBasicMaterial({vertexColors: true, transparent: true, opacity: .5})));
    }
    if (source !== receiver) {
      const geometry = new T.BufferGeometry().setFromPoints([point(source), receiverPoint]);
      const line = new T.Line(geometry, new T.LineDashedMaterial({color: '#ffffff', dashSize: .05, gapSize: .035, transparent: true, opacity: .85}));
      line.computeLineDistances(); links.add(line);
    }
    visibility(); render();
  }
  function setFrame(nextFrame, recenter = false) {
    if (!nextFrame.poses) throw Error('No original saved poses for selected origin');
    frame = nextFrame; shift.set(...(recenter ? frame.origin : [0, 0, 0])); box.makeEmpty();
    for (let id = 0; id < N; id++) {
      position.copy(point(id)); box.expandByPoint(position);
      quaternion.set(frame.poses[id * 17 + 6], frame.poses[id * 17 + 7], frame.poses[id * 17 + 8], frame.poses[id * 17 + 9]);
      matrix.compose(position, quaternion, scale); body.setMatrixAt(id, matrix);
      for (let arm = 0; arm < 2; arm++) {
        const rotation = quaternion.clone().multiply(new T.Quaternion().setFromAxisAngle(new T.Vector3(0, 0, 1), arm ? -Math.PI / 4 : Math.PI / 4));
        matrix.compose(position, rotation, scale); arms.setMatrixAt(2 * id + arm, matrix);
      }
    }
    bodyMatrices = body.instanceMatrix.array.slice(); armMatrices = arms.instanceMatrix.array.slice(); receiverPoint = point(selectedReceiver);
    document.body.dataset.displayOrigin = recenter ? frame.origin.join(',') : '0,0,0';
    if (lastShow) show(lastShow); else visibility();
  }
  let pointer;
  const pointerDown = event => {pointer = [event.clientX, event.clientY];};
  const pointerUp = event => {
    const started = pointer; pointer = null;
    if (!started || Math.hypot(event.clientX - started[0], event.clientY - started[1]) > 5) return;
    const bounds = renderer.domElement.getBoundingClientRect(), ray = new T.Raycaster();
    ray.setFromCamera(new T.Vector2(2 * (event.clientX - bounds.left) / bounds.width - 1, 1 - 2 * (event.clientY - bounds.top) / bounds.height), camera);
    const hit = ray.intersectObject(body)[0]; if (hit?.instanceId !== undefined) onSource(hit.instanceId);
  };
  renderer.domElement.addEventListener('pointerdown', pointerDown); renderer.domElement.addEventListener('pointerup', pointerUp);
  orbit.addEventListener('change', render);
  setFrame(initialFrame);
  const resize = new ResizeObserver(() => {
    const width = host.clientWidth, height = host.clientHeight;
    if (!width || !height || disposed) return;
    renderer.setSize(width, height, false);camera.aspect = width / height;camera.updateProjectionMatrix();fit();
  });resize.observe(host);
  function dispose() {
    disposed = true;resize.disconnect();orbit.removeEventListener('change', render);orbit.dispose();
    renderer.domElement.removeEventListener('pointerdown', pointerDown);renderer.domElement.removeEventListener('pointerup', pointerUp);
    clear(markers);clear(links);body.geometry.dispose();body.material.dispose();arms.geometry.dispose();arms.material.dispose();renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();
  }
  return {show, fit, render, setFrame, dispose};
}
