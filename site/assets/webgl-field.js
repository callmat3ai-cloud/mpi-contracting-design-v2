/* Decorative copper contour field for the hero panel.
   Lazy-loaded, DPR-capped, paused when hidden or offscreen, absent under reduced motion. */
import * as THREE from './vendor/three.module.min.js';

const FRAG = `
precision mediump float;
uniform vec2 uRes;
uniform float uTime;
varying vec2 vUv;

float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }
float vnoise(vec2 p){
  vec2 i = floor(p), f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
             mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}
float fbm(vec2 p){
  float v = 0.0, a = 0.5;
  for (int i = 0; i < 3; i++){ v += a * vnoise(p); p *= 2.05; a *= 0.5; }
  return v;
}

void main(){
  vec2 uv = vUv;
  uv.x *= uRes.x / max(uRes.y, 1.0);
  float t = uTime * 0.035;
  // slow, wide survey lines rather than a marbled field
  float field = fbm(uv * 1.15 + vec2(t * 0.5, -t * 0.3));
  field += 0.22 * fbm(uv * 3.1 - vec2(t * 0.18, t * 0.42));
  float band = abs(fract(field * 5.0) - 0.5);
  float line = smoothstep(0.022, 0.0, band);
  float hair = smoothstep(0.006, 0.0, abs(fract(field * 5.0 + 0.5) - 0.5));
  float fade = smoothstep(0.0, 0.55, vUv.y) * smoothstep(1.0, 0.72, vUv.y);
  fade *= smoothstep(0.0, 0.22, vUv.x);              // recede behind the headline
  vec3 copper = vec3(0.780, 0.412, 0.243);
  float a = (line * 0.16 + hair * 0.05) * fade;
  gl_FragColor = vec4(copper, a);
}
`;

const VERT = `
varying vec2 vUv;
void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }
`;

export function mount(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));

  const scene = new THREE.Scene();
  const camera = new THREE.Camera();
  const uniforms = {
    uRes: { value: new THREE.Vector2(1, 1) },
    uTime: { value: 0 },
  };
  const quad = new THREE.Mesh(
    new THREE.PlaneGeometry(2, 2),
    new THREE.ShaderMaterial({ vertexShader: VERT, fragmentShader: FRAG, uniforms, transparent: true, depthTest: false })
  );
  scene.add(quad);

  const resize = () => {
    const w = canvas.clientWidth || 1;
    const h = canvas.clientHeight || 1;
    renderer.setSize(w, h, false);
    uniforms.uRes.value.set(w * renderer.getPixelRatio(), h * renderer.getPixelRatio());
  };
  resize();
  window.addEventListener('resize', resize, { passive: true });

  let visible = true;
  let raf = 0;
  const clock = new THREE.Clock();

  const loop = () => {
    raf = requestAnimationFrame(loop);
    uniforms.uTime.value = clock.getElapsedTime();
    renderer.render(scene, camera);
  };
  const start = () => { if (!raf) { clock.start(); loop(); } };
  const stop = () => { if (raf) { cancelAnimationFrame(raf); raf = 0; } };

  const io = new IntersectionObserver((entries) => {
    visible = entries.some((e) => e.isIntersecting);
    visible && !document.hidden ? start() : stop();
  }, { threshold: 0.01 });
  io.observe(canvas);
  document.addEventListener('visibilitychange', () => {
    document.hidden || !visible ? stop() : start();
  });

  return Promise.resolve();
}
