import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';

// Each cube is one saved-byte comparison. Position/height never encode motion or flight.
export function createByteScene(container, onSelect) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x0c1420);
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 120);
  const renderer = new THREE.WebGLRenderer({antialias: true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.domElement.setAttribute('aria-label', '128 byte cells arranged into 32 words; an accessible word selector and byte table follow');
  container.replaceChildren(renderer.domElement);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = false; controls.enablePan = false;
  controls.minDistance = 10; controls.maxDistance = 80;
  controls.maxPolarAngle = Math.PI * 0.47;
  const colors = {match: 0x6ac3ac, mismatch: 0xee8c74, unknown: 0x64758a};
  const regionColors = {prefix: 0xb7a8e8, active: 0x8dc9ed, suffix: 0xd7b37c};
  const cubes = [], bases = [], pickable = [];
  scene.add(new THREE.HemisphereLight(0xd1e6ff, 0x233a50, 3));
  const light = new THREE.DirectionalLight(0xffffff, 2.2); light.position.set(3, 8, 5); scene.add(light);
  const grid = new THREE.GridHelper(24, 24, 0x263e53, 0x192c3e); grid.position.y = -0.4; scene.add(grid);
  const geometry = new THREE.BoxGeometry(0.42, 0.48, 0.72);
  for (let word = 0; word < 32; word++) {
    const x = (word % 8 - 3.5) * 2.35, z = (Math.floor(word / 8) - 1.5) * 2.25;
    const region = word < 4 ? 'prefix' : word < 21 ? 'active' : 'suffix';
    const base = new THREE.Mesh(new THREE.BoxGeometry(2.02, 0.08, 1.08), new THREE.MeshStandardMaterial({color: regionColors[region], transparent: true, opacity: 0.25, roughness: 0.7}));
    base.position.set(x, -0.19, z); base.userData.word = word; bases.push(base); scene.add(base);
    for (let byte = 0; byte < 4; byte++) {
      const cube = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({color: colors.unknown, roughness: 0.55}));
      cube.position.set(x + (byte - 1.5) * 0.47, 0.1, z);
      cube.userData = {word, offset: word * 4 + byte}; cubes.push(cube); pickable.push(cube); scene.add(cube);
    }
    const canvas = document.createElement('canvas'); canvas.width = 128; canvas.height = 64;
    const context = canvas.getContext('2d'); context.fillStyle = '#c0d0e1'; context.font = '500 34px system-ui'; context.textAlign = 'center'; context.fillText(String(word).padStart(2, '0'), 64, 43);
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({map: new THREE.CanvasTexture(canvas), transparent: true, depthTest: false}));
    sprite.scale.set(0.8, 0.4, 1); sprite.position.set(x, 0.62, z - 0.18); scene.add(sprite);
  }
  function render() { renderer.render(scene, camera); }
  function reset() {
    const width = Math.max(1, container.clientWidth), height = Math.max(1, container.clientHeight);
    const aspect = width / height;
    const distance = Math.max(21, 11.3 / (Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * aspect));
    camera.position.set(0, distance * 0.68, distance * 0.733);
    camera.up.set(0, 1, 0); controls.target.set(0, 0, 0); controls.update(); render();
  }
  const observer = new ResizeObserver(() => {
    const width = Math.max(1, container.clientWidth), height = Math.max(1, container.clientHeight);
    renderer.setSize(width, height); camera.aspect = width / height; camera.updateProjectionMatrix(); reset();
  });
  observer.observe(container); controls.addEventListener('change', render);
  let down = null;
  renderer.domElement.addEventListener('pointerdown', event => { down = {x: event.clientX, y: event.clientY}; });
  renderer.domElement.addEventListener('pointerup', event => {
    if (!down || Math.hypot(event.clientX - down.x, event.clientY - down.y) > 5) { down = null; return; }
    down = null;
    const bounds = renderer.domElement.getBoundingClientRect(), ray = new THREE.Raycaster();
    ray.setFromCamera(new THREE.Vector2((event.clientX - bounds.left) / bounds.width * 2 - 1, -(event.clientY - bounds.top) / bounds.height * 2 + 1), camera);
    const hit = ray.intersectObjects(pickable)[0]; if (hit) onSelect(hit.object.userData.word);
  });
  renderer.domElement.addEventListener('pointercancel', () => { down = null; });
  function update(states, selected) {
    cubes.forEach((cube, index) => {
      cube.material.color.setHex(colors[states[index]] ?? colors.unknown);
      cube.material.emissive.setHex(cube.userData.word === selected ? 0x14364b : 0x000000);
    });
    bases.forEach((base, index) => { base.material.opacity = index === selected ? 0.75 : 0.25; }); render();
  }
  reset();
  return {reset, update, dispose() {
    observer.disconnect(); controls.dispose();
    const geometries = new Set(), materials = new Set(), textures = new Set();
    scene.traverse(item => { if (item.geometry) geometries.add(item.geometry); for (const material of item.material ? [].concat(item.material) : []) { materials.add(material); if (material.map) textures.add(material.map); } });
    for (const item of textures) item.dispose(); for (const item of materials) item.dispose(); for (const item of geometries) item.dispose();
    renderer.dispose(); container.replaceChildren();
  }};
}
