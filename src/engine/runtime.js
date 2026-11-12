/**
 * Minimal webpack-compatible module runtime.
 *
 * The site's original application modules (src/engine/chunks/*.js) are kept
 * verbatim so every shader, damping constant, easing curve and timing matches
 * the live site exactly. Vendor modules they import by numeric id are mapped
 * here to the real npm packages (three, @react-three/fiber, gsap, framer-motion…).
 */
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as JSX from 'react/jsx-runtime';
import * as THREE from 'three';
import { Canvas, useThree, useFrame, useLoader } from '@react-three/fiber';
import { useTexture } from '@react-three/drei';
import gsap from 'gsap';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import Lenis from 'lenis';
import { createStore } from 'zustand/vanilla';
import { Toaster } from 'react-hot-toast';
import { usePathname, useRouter } from './navigation';

// Register original chunks (they push into this global like webpack does).
self.webpackChunk_N_E = self.webpackChunk_N_E || [];

/** Strict proxy: throws if the original code reaches for an export we did not map. */
function strict(name, map) {
  return new Proxy(map, {
    get(target, key) {
      if (key in target) return target[key];
      if (typeof key === 'symbol' || key === '__esModule' || key === 'then') return undefined;
      throw new Error(`[runtime] unmapped export "${String(key)}" on vendor module ${name}`);
    },
  });
}

const externals = {
  2115: React,
  5155: JSX,
  7650: ReactDOM,
  3264: strict('three', {
    cj9: THREE.MathUtils,
    Pq0: THREE.Vector3,
    I9Y: THREE.Vector2,
    ubm: THREE.PerspectiveCamera,
    Nv2: THREE.VideoTexture,
    er$: THREE.SRGBColorSpace,
    k6q: THREE.LinearFilter,
    $EB: THREE.DoubleSide,
    eaF: THREE.Mesh,
    BKk: THREE.ShaderMaterial,
    Q1f: THREE.Color,
    h_9: THREE.DefaultLoadingManager,
    Tap: THREE.TextureLoader,
    gPd: THREE.Texture,
    // used by the 404 scene
    Z58: THREE.Scene,
    YJl: THREE.Group,
    GOR: THREE.CanvasTexture,
    V9B: THREE.MeshBasicMaterial,
    bdM: THREE.PlaneGeometry,
    zD7: THREE.Clock,
  }),
  7431: strict('three/renderer', { WebGLRenderer: THREE.WebGLRenderer }),
  3967: strict('fiber', { A: useThree, C: useFrame, F: useLoader }),
  7558: strict('fiber-canvas', { Hl: Canvas }),
  2660: strict('drei', { zo: useTexture }),
  802: strict('gsap', { Ay: gsap, default: gsap }),
  6799: strict('framer-motion', { P: motion }),
  9400: strict('framer-motion/AnimatePresence', { N: AnimatePresence }),
  3084: strict('framer-motion/useReducedMotion', { I: useReducedMotion }),
  5695: strict('next/navigation', { usePathname, useRouter }),
  2810: strict('lenis', { A: Lenis }),
  2421: strict('zustand', { y: createStore }),
  3568: strict('react-hot-toast', { Toaster }),
  8229: { _: (m) => (m && m.__esModule ? m : { default: m }) },
  // Next.js internals referenced by next/dynamic plumbing — inert here.
  589: {},
  5262: {},
};

const factories = {};
const cache = {};

function collect() {
  for (const entry of self.webpackChunk_N_E) {
    const mods = entry[1] || {};
    for (const id of Object.keys(mods)) if (!(id in factories)) factories[id] = mods[id];
  }
}

export function require(id) {
  if (id in externals) return externals[id];
  if (id in cache) return cache[id].exports;
  collect();
  const factory = factories[id];
  if (!factory) throw new Error(`[runtime] missing module ${id}`);
  const module = (cache[id] = { exports: {} });
  factory.call(module.exports, module, module.exports, require);
  return module.exports;
}

// webpack helpers used by the original modules
require.d = (exports, defs) => {
  for (const k in defs)
    if (!Object.prototype.hasOwnProperty.call(exports, k))
      Object.defineProperty(exports, k, { enumerable: true, get: defs[k] });
};
require.r = (exports) => {
  if (typeof Symbol !== 'undefined' && Symbol.toStringTag)
    Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
  Object.defineProperty(exports, '__esModule', { value: true });
};
require.e = () => Promise.resolve(); // chunks are already bundled by Vite
require.t = (id) => require(id);
require.n = (module) => {
  const getter = module && module.__esModule ? () => module.default : () => module;
  require.d(getter, { a: getter });
  return getter;
};
require.o = (o, k) => Object.prototype.hasOwnProperty.call(o, k);
