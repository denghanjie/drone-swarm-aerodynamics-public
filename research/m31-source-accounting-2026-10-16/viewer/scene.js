import * as THREE from 'three';
import { OrbitControls } from '../../../outputs/step02b-source/vendor/OrbitControls.js';

const SPEED = { bothFades: 'bothFadesMps', radialOnly: 'radialOnlyMps', untruncated: 'untruncatedMps' };

export function createProfileScene(host, planes, D, colorMax) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x102031, 1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  host.replaceChildren(renderer.domElement);
  const overlay = document.createElement('div');
  Object.assign(overlay.style, { position: 'absolute', left: '16px', top: '14px', right: '16px', color: '#d7e7ed', fontSize: '12px', lineHeight: '1.5', pointerEvents: 'none' });
  host.append(overlay);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.01, 50);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = false; controls.autoRotate = false;
  controls.minDistance = 1; controls.maxDistance = 15; controls.enablePan = true;
  controls.listenToKeyEvents(host);
  const slices = new THREE.Group(); scene.add(slices);
  const guides = new THREE.Group(); scene.add(guides);
  const maxR = Math.max(...planes.map(p => p.profile[p.profile.length - 1].radiusM));
  const maxS = planes[planes.length - 1].downstreamM;
  const cold = new THREE.Color('#2287a2'), middle = new THREE.Color('#47b8ba'), warm = new THREE.Color('#f6b451');
  const shade = value => {
    const t = Math.max(0, Math.min(1, value / Math.max(colorMax, Number.EPSILON)));
    return t < 0.5 ? cold.clone().lerp(middle, t * 2) : middle.clone().lerp(warm, (t - 0.5) * 2);
  };
  function line(points, color = 0x77909f, dashed = false) {
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = dashed ? new THREE.LineDashedMaterial({ color, dashSize: 0.035, gapSize: 0.025, transparent: true, opacity: 0.6 }) : new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.65 });
    const item = new THREE.Line(geometry, material); if (dashed) item.computeLineDistances(); return item;
  }
  function label(text, x, y, z, color = '#bed0db') {
    const canvas = document.createElement('canvas'); canvas.width = 640; canvas.height = 64;
    const context = canvas.getContext('2d'); context.font = '28px system-ui, sans-serif'; context.fillStyle = color;
    context.textAlign = 'center'; context.textBaseline = 'middle'; context.fillText(text, 320, 32);
    const texture = new THREE.CanvasTexture(canvas); texture.colorSpace = THREE.SRGBColorSpace;
    const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false });
    const item = new THREE.Sprite(material); item.position.set(x, y, z); item.scale.set(1.32, 0.132, 1); return item;
  }
  guides.add(line([new THREE.Vector3(0, 0.1, 0), new THREE.Vector3(0, -maxS - 0.25, 0)]));
  guides.add(line([new THREE.Vector3(-maxR, -maxS - 0.12, 0), new THREE.Vector3(maxR, -maxS - 0.12, 0)]));
  guides.add(label('source axis · s = 0', 0, 0.19, 0));
  guides.add(label('downstream s / m', 0, -maxS - 0.36, 0));
  guides.add(label('radial r / m', maxR * 0.75, -maxS - 0.23, 0));
  guides.add(line([new THREE.Vector3(-D, -2.5 * D, 0), new THREE.Vector3(D, -2.5 * D, 0)], 0xabb6c1, true));
  // This guide only positions the declared 2.5D domain boundary; it evaluates no flow.
  function clearSlices() {
    for (const item of [...slices.children]) {
      slices.remove(item); item.geometry?.dispose();
      if (item.material?.map) item.material.map.dispose();
      item.material?.dispose();
    }
  }
  function ring(radius, y) {
    return Array.from({ length: 65 }, (_, k) => {
      const angle = k / 64 * 2 * Math.PI;
      return new THREE.Vector3(radius * Math.cos(angle), y, radius * Math.sin(angle));
    });
  }
  function addSlice(plane, selected, speedKey) {
    const samples = plane.profile;
    const positions = [], colors = [], indices = [], sectors = 48;
    for (const point of samples) {
      const color = shade(point[speedKey]);
      for (let k = 0; k <= sectors; k++) {
        const angle = k / sectors * 2 * Math.PI;
        positions.push(point.radiusM * Math.cos(angle), -plane.downstreamM, point.radiusM * Math.sin(angle));
        colors.push(color.r, color.g, color.b);
      }
    }
    for (let r = 0; r < samples.length - 1; r++) {
      if (samples[r][speedKey] === 0 && samples[r + 1][speedKey] === 0) continue;
      for (let k = 0; k < sectors; k++) {
        const a = r * (sectors + 1) + k, b = a + sectors + 1;
        indices.push(a, b, a + 1, b, b + 1, a + 1);
      }
    }
    if (indices.length) {
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
      geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
      geometry.setIndex(indices);
      const material = new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide, transparent: true, opacity: selected ? 0.9 : 0.2, depthWrite: false });
      const mesh = new THREE.Mesh(geometry, material); mesh.renderOrder = selected ? 2 : 1; slices.add(mesh);
    }
    if (selected) {
      slices.add(line(ring(samples[samples.length - 1].radiusM, -plane.downstreamM), 0xc6d6df, true));
      slices.add(label(`selected s = ${plane.downstreamM} m`, 0, -plane.downstreamM + 0.1, samples[samples.length - 1].radiusM + 0.12, '#eff9fc'));
    }
  }
  function render() { renderer.render(scene, camera); }
  function resize() {
    const width = Math.max(1, host.clientWidth), height = Math.max(1, host.clientHeight);
    renderer.setSize(width, height, false); camera.aspect = width / height; camera.updateProjectionMatrix(); render();
  }
  function reset() {
    camera.position.set(maxR * 2.6 + 0.8, 1.2, maxS * 1.7);
    controls.target.set(0, -maxS / 2, 0); controls.update(); render();
  }
  controls.addEventListener('change', render);
  const observer = new ResizeObserver(resize); observer.observe(host);
  renderer.domElement.addEventListener('webglcontextlost', event => {
    event.preventDefault(); overlay.textContent = '3D context unavailable. Use the verified radial plot and numeric tables below.';
  });
  reset(); resize();
  return {
    reset,
    setState(index, modeKey, modeLabel) {
      clearSlices();
      planes.forEach((plane, i) => addSlice(plane, i === index, SPEED[modeKey]));
      const empty = modeKey === 'bothFades' && planes[index].fadedFieldIdenticallyZero;
      overlay.textContent = `${modeLabel} · ${planes.length} recorded planes${empty ? ' · selected field empty' : ''}`;
      host.setAttribute('aria-label', `${modeLabel}. Selected downstream plane ${planes[index].downstreamM} metres${empty ? ', saved field identically zero' : ''}. Static saved scalar-profile slices; numeric tables below provide the same data.`);
      render();
    },
    dispose() { observer.disconnect(); controls.dispose(); clearSlices(); renderer.dispose(); },
  };
}
