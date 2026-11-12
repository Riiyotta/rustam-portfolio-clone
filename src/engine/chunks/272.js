"use strict";
(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
  [272],
  {
    5272: (e, t, n) => {
      (n.r(t), n.d(t, { default: () => ep }));
      var r = n(5155),
        i = n(7558),
        l = n(5695),
        a = n(802),
        o = n(2115),
        u = n(3967),
        s = n(2660),
        c = n(3264);
      let d =
        "\n  uniform sampler2D uTexture;\n  uniform sampler2D uNextTexture;\n  uniform sampler2D uCoverTexture;\n\n  uniform vec2 uUvFromScale, uUvFromOffset;\n  uniform vec2 uUvToScale, uUvToOffset;\n  uniform vec2 uUvCoverScale, uUvCoverOffset;\n\n  uniform float uMorph, uCoverReturn, uOpacity, uTime, uBlur;\n  uniform vec2 uImageSize;\n\n  varying vec2 vUv;\n\n  // Background for transparent PNG pixels.\n  // Linear RGB equivalent of approximately #f1f0f0.\n  const vec3 ALPHA_BACKGROUND =\n    vec3(0.88, 0.871, 0.871);\n\n  vec4 compositeAlpha(vec4 color) {\n    float alpha = clamp(color.a, 0.0, 1.0);\n\n    vec3 rgb = mix(\n      ALPHA_BACKGROUND,\n      color.rgb,\n      alpha\n    );\n\n    return vec4(rgb, 1.0);\n  }\n\n  float hash(vec2 p) {\n    return fract(\n      sin(dot(p, vec2(127.1, 311.7))) *\n      43758.5453123\n    );\n  }\n\n  float noise(vec2 p) {\n    vec2 i = floor(p);\n    vec2 f = fract(p);\n    vec2 u = f * f * (3.0 - 2.0 * f);\n\n    return mix(\n      mix(\n        hash(i),\n        hash(i + vec2(1.0, 0.0)),\n        u.x\n      ),\n      mix(\n        hash(i + vec2(0.0, 1.0)),\n        hash(i + vec2(1.0, 1.0)),\n        u.x\n      ),\n      u.y\n    );\n  }\n\n  void main() {\n    float p = clamp(uMorph, 0.0, 1.0);\n\n    if (\n      p <= 0.0001 &&\n      uCoverReturn <= 0.0001\n    ) {\n      vec2 uv = clamp(\n        vUv * uUvFromScale + uUvFromOffset,\n        0.002,\n        0.998\n      );\n\n      vec4 color = compositeAlpha(\n        texture2D(uTexture, uv)\n      );\n\n      if (uBlur > 0.001) {\n        float amount = clamp(\n          uBlur,\n          0.0,\n          1.0\n        );\n\n        vec4 softened = compositeAlpha(\n          texture2D(uTexture, uv, 1.4 * amount)\n        );\n\n        color.rgb = mix(\n          color.rgb,\n          softened.rgb,\n          amount * 0.78\n        );\n\ncolor.rgb *= 1.0 - 0.60 * amount;      }\n\n      gl_FragColor = vec4(\n        color.rgb,\n        uOpacity\n      );\n\n      #include <tonemapping_fragment>\n      #include <colorspace_fragment>\n\n      return;\n    }\n\n    vec2 flow = vec2(\n      noise(\n        vUv * vec2(3.0, 4.5) +\n        vec2(uTime * 0.08, -p)\n      ) - 0.5,\n      noise(\n        vUv * vec2(4.2, 3.1) +\n        vec2(p, uTime * 0.06)\n      ) - 0.5\n    );\n\n    flow += vec2(\n      sin(\n        vUv.y * 12.0 +\n        vUv.x * 3.0 -\n        p * 3.14159265\n      ),\n      cos(\n        vUv.x * 9.0 -\n        vUv.y * 4.0 +\n        p * 3.14159265\n      )\n    ) * 0.22;\n\n    vec2 fromUv = clamp(\n      (vUv + flow * 0.20 * p) *\n      uUvFromScale + uUvFromOffset,\n      0.002,\n      0.998\n    );\n\n    vec2 toUv = clamp(\n      (\n        vUv -\n        flow * 0.20 * (1.0 - p)\n      ) * uUvToScale + uUvToOffset,\n      0.002,\n      0.998\n    );\n\n    // Composite both textures individually before\n    // the morph to avoid transparent regions showing\n    // the dark gallery background.\n\n    vec4 fromColor = compositeAlpha(\n      texture2D(uTexture, fromUv)\n    );\n\n    vec4 toColor = compositeAlpha(\n      texture2D(uNextTexture, toUv)\n    );\n\n    float reveal = smoothstep(\n      0.0,\n      1.0,\n      p\n    );\n\n    vec4 color = mix(\n      fromColor,\n      toColor,\n      reveal\n    );\n\n    vec2 coverUv = clamp(\n      (\n        vUv +\n        flow * 0.09 *\n        uCoverReturn *\n        (1.0 - uCoverReturn)\n      ) * uUvCoverScale + uUvCoverOffset,\n      0.002,\n      0.998\n    );\n\n    vec4 coverColor = compositeAlpha(\n      texture2D(uCoverTexture, coverUv)\n    );\n\n    color = mix(\n      color,\n      coverColor,\n      uCoverReturn\n    );\n\n    gl_FragColor = vec4(\n      color.rgb,\n      uOpacity\n    );\n\n    #include <tonemapping_fragment>\n    #include <colorspace_fragment>\n  }\n";
      function p(e) {
        let t = c.cj9.clamp(e, 0, 1);
        return t * t * (3 - 2 * t);
      }
      function v(e, t, n, r, i) {
        e.updateWorldMatrix(!0, !1);
        let l = e.localToWorld(new c.Pq0(-(0.48 * r), 0.5 * i, 0.12));
        l.project(t);
        let a = (l.x + 1) * n.width * 0.5,
          o = (1 - l.y) * n.height * 0.5,
          u = Math.max(0.1, t.position.z - e.position.z),
          s =
            t instanceof c.ubm
              ? n.height / (2 * Math.tan(c.cj9.degToRad(t.fov / 2)) * u)
              : 1,
          d = r * e.scale.x * s,
          p = c.cj9.clamp(0.048 * d, 11, 16);
        return {
          x: a,
          y: o - 12 - 0.52 * p,
          font: p,
          width: Math.max(90, 0.87 * d),
          yaw: e.rotation.y,
          pitch: e.rotation.x,
        };
      }
      let h = [0.14, 0.18, 0.13, 0.16, 0.15, 0.19],
        m = 0.13 / 0.15;
      function f(e) {
        let {
            projects: t,
            scrollTarget: n,
            profileActive: i,
            selected: l,
            progress: a,
            onHoverChange: f,
            pressedPlaneRef: x,
            titleRef: g,
            closingRef: w,
            backdropRef: y,
            imageProgress: b,
            mediaJump: M,
            coverMorph: j,
            imageHitTestRef: T,
            listHitTestRef: P,
            pointerPositionRef: C,
            initialProjectIndex: k = -1,
          } = e,
          { camera: S, size: N, gl: I } = (0, u.A)(),
          R = N.width < 768,
          E = (0, o.useMemo)(
            () =>
              t.map((e) => {
                var t;
                return [
                  e.src,
                  ...(null != (t = e.images) ? t : []).filter(
                    (t) => t && t !== e.src,
                  ),
                ];
              }),
            [t],
          ),
          A = (0, o.useMemo)(
            () =>
              E.map((e, n) => {
                var r, i;
                let l = e.map((e) => ({ kind: "image", src: e })),
                  a =
                    null == (i = t[n]) || null == (r = i.srcVideo)
                      ? void 0
                      : r.trim();
                return (a && l.push({ kind: "video", src: a }), l);
              }),
            [E, t],
          ),
          O = (0, o.useMemo)(() => [...new Set(E.flat())], [E]),
          U = (0, s.zo)(O),
          L = (0, o.useMemo)(() => new Map(O.map((e, t) => [e, U[t]])), [O, U]),
          z = (0, o.useMemo)(() => E.map((e) => L.get(e[0])), [E, L]),
          B = (0, o.useRef)([]),
          D = (0, o.useRef)(0),
          H = (0, o.useRef)(!1),
          F = (0, o.useRef)(!1),
          W = (0, o.useRef)(null),
          Y = (0, o.useRef)(null),
          X = (0, o.useRef)([]),
          G = (0, o.useRef)(null),
          _ = (0, o.useRef)(new c.Pq0()),
          q = (0, o.useRef)([]);
        (0, o.useEffect)(
          () => (
            (T.current = (e, t) => {
              let n = q.current;
              if (n.length < 6) return !1;
              let r = !1,
                i = n.length / 2;
              for (let l = 0, a = i - 1; l < i; a = l++) {
                let i = n[2 * l],
                  o = n[2 * l + 1],
                  u = n[2 * a],
                  s = n[2 * a + 1];
                o > t != s > t &&
                  e < ((u - i) * (t - o)) / (s - o) + i &&
                  (r = !r);
              }
              return r;
            }),
            () => {
              T.current = null;
            }
          ),
          [T],
        );
        let {
          videoElementRef: V,
          videoTextureRef: $,
          videoPlayRequestedRef: K,
        } = (function (e, t) {
          let n = (0, o.useRef)(null),
            r = (0, o.useRef)(null),
            i = (0, o.useRef)(!1);
          return (
            (0, o.useEffect)(() => {
              var l, a;
              let o = e
                ? null == (a = t[e.index]) || null == (l = a.srcVideo)
                  ? void 0
                  : l.trim()
                : null;
              if (!o) return;
              let u = document.createElement("video");
              ((u.crossOrigin = "anonymous"),
                (u.muted = !0),
                (u.defaultMuted = !0),
                (u.loop = !0),
                (u.playsInline = !0),
                (u.preload = "auto"),
                u.setAttribute("playsinline", "true"),
                u.setAttribute("webkit-playsinline", "true"),
                (u.src = o));
              let s = new c.Nv2(u);
              return (
                (s.colorSpace = c.er$),
                (s.minFilter = c.k6q),
                (s.magFilter = c.k6q),
                (s.generateMipmaps = !1),
                (n.current = u),
                (r.current = s),
                (i.current = !1),
                u.load(),
                () => {
                  (u.pause(),
                    u.removeAttribute("src"),
                    u.load(),
                    s.dispose(),
                    n.current === u && (n.current = null),
                    r.current === s && (r.current = null),
                    (i.current = !1));
                }
              );
            }, [null == e ? void 0 : e.index, t]),
            { videoElementRef: n, videoTextureRef: r, videoPlayRequestedRef: i }
          );
        })(l, t);
        (0, o.useEffect)(() => {
          U.forEach((e) => {
            ((e.colorSpace = c.er$), (e.anisotropy = 4), (e.needsUpdate = !0));
          });
        }, [U]);
        let { planes: J, totalWidth: Q } = (0, o.useMemo)(() => {
          let e = N.width * (R ? 0.035 : 0.012),
            t = 0,
            n = z.map((n, r) => {
              let i = n.image,
                l =
                  ((null == i ? void 0 : i.width) || 16) /
                  ((null == i ? void 0 : i.height) || 9),
                a = N.height * h[r % h.length] * (R ? m : 1),
                o = a * l,
                u = t + o / 2;
              return ((t += o + e), { index: r, width: o, height: a, x: u });
            }),
            r = t,
            i = Math.ceil(N.width / Math.max(r, 1)) + 2;
          return {
            planes: n.flatMap((e) =>
              Array.from({ length: 2 * i + 1 }, (t, n) => ({
                ...e,
                copy: n - i,
              })),
            ),
            totalWidth: r,
          };
        }, [z, N.width, N.height, R]);
        (0, o.useEffect)(
          () => (
            (P.current = function (e, t) {
              let r =
                arguments.length > 2 && void 0 !== arguments[2] && arguments[2];
              if (Q <= 0) return null;
              let i = I.domElement.getBoundingClientRect();
              if (
                i.width <= 0 ||
                i.height <= 0 ||
                e < i.left ||
                e > i.right ||
                t < i.top ||
                t > i.bottom
              )
                return null;
              let l = ((e - i.left) / i.width - 0.5) * N.width,
                a = (0.5 - (t - i.top) / i.height) * N.height,
                o = -(0.48 * N.height),
                u = c.cj9.euclideanModulo(D.current, Q);
              for (let e = J.length - 1; e >= 0; e--) {
                let t = J[e],
                  i = t.x + t.copy * Q - u,
                  s = o + t.height / 2;
                if (
                  Math.abs(l - i) <= 0.5 * t.width &&
                  Math.abs(a - s) <= 0.5 * t.height
                )
                  return (
                    r && (n.current = D.current),
                    { index: t.index, copy: t.copy }
                  );
              }
              return null;
            }),
            () => {
              P.current = null;
            }
          ),
          [I, P, J, n, N.height, N.width, Q],
        );
        let Z = (0, o.useMemo)(
          () =>
            J.map((e) => {
              let t = z[e.index];
              return {
                uTexture: { value: t },
                uNextTexture: { value: t },
                uCoverTexture: { value: t },
                uMorph: { value: 0 },
                uEdgeMorphStrength: { value: 0.22 },
                uCoverReturn: { value: 0 },
                uUvFromScale: { value: new c.I9Y(1, 1) },
                uUvFromOffset: { value: new c.I9Y(0, 0) },
                uUvToScale: { value: new c.I9Y(1, 1) },
                uUvToOffset: { value: new c.I9Y(0, 0) },
                uUvCoverScale: { value: new c.I9Y(1, 1) },
                uUvCoverOffset: { value: new c.I9Y(0, 0) },
                uTime: { value: 0 },
                uHover: { value: 0 },
                uBlur: { value: 0 },
                uWorldScale: { value: e.height / 3.6 },
                uImageSize: { value: new c.I9Y(e.width, e.height) },
                uEdgeBend: { value: 0 },
                uTransitionBend: { value: 0 },
                uPointer: { value: new c.I9Y() },
                uMotion: { value: new c.I9Y() },
                uOpacity: { value: 1 },
              };
            }),
          [J, z],
        );
        return (
          (0, u.C)((e, r) => {
            var o, u, s, d, h, m, T, O, U, Z, ee, et, en, er, ei;
            if (Q <= 0) return;
            if (!H.current && ((H.current = !0), k >= 0 && k < t.length)) {
              let e = J.find((e) => e.index === k && 0 === e.copy);
              e && ((D.current = e.x), (n.current = e.x));
            }
            let el = Math.min(r, 0.05);
            (null !== l &&
              ((null == (o = W.current) ? void 0 : o.index) !== l.index ||
                (null == (u = W.current) ? void 0 : u.copy) !== l.copy) &&
              ((W.current = l), (n.current = D.current), (G.current = null)),
              l ||
                (W.current && (Y.current = null),
                (W.current = null),
                (G.current = null),
                (D.current = c.cj9.damp(D.current, n.current, 9, el))));
            let ea = Q / 1;
            if (!l && Math.abs(D.current) > 20 * ea) {
              let e = Math.trunc(D.current / ea) * ea;
              ((D.current -= e), (n.current -= e));
            }
            let eo = c.cj9.euclideanModulo(+D.current, Q);
            if (l || i || R) Y.current && (Y.current = null);
            else {
              let e = C.current,
                t =
                  e &&
                  null !=
                    (d = null == (s = P.current) ? void 0 : s.call(P, e.x, e.y))
                    ? d
                    : null,
                n = Y.current;
              ((null == n ? void 0 : n.index) !==
                (null == t ? void 0 : t.index) ||
                (null == n ? void 0 : n.copy) !==
                  (null == t ? void 0 : t.copy)) &&
                ((Y.current = t), f(t));
            }
            if (l && !G.current && F.current) {
              let t = J.findIndex(
                  (e) => e.index === l.index && e.copy === l.copy,
                ),
                n = B.current[t],
                r = J[t];
              if (n && r) {
                let t = n.material.uniforms;
                ((G.current = {
                  index: l.index,
                  copy: l.copy,
                  position: n.position.clone(),
                  scale: n.scale.clone(),
                  rotation: n.rotation.clone(),
                  pointer: t.uPointer.value.clone(),
                  motion: t.uMotion.value.clone(),
                  hover: t.uHover.value,
                  edgeBend: t.uEdgeBend.value,
                  title: v(n, e.camera, N, r.width, r.height),
                }),
                  (x.current = null));
              }
            }
            let eu = c.cj9.clamp(a.current.value, 0, 1),
              es = V.current;
            if (es && l) {
              let e =
                  (null != (m = null == (h = A[l.index]) ? void 0 : h.length)
                    ? m
                    : 1) - 1,
                t =
                  !w.current &&
                  eu > 0.97 &&
                  e >= 1 &&
                  (M.current
                    ? M.current.from === e ||
                      (M.current.to === e && M.current.progress > 0.001)
                    : b.current.value >= e - 0.99);
              t && es.paused && !K.current
                ? ((K.current = !0),
                  es.play().catch(() => {
                    K.current = !1;
                  }))
                : t || (es.paused || es.pause(), (K.current = !1));
            }
            let ec = p(eu),
              ed = Math.sin(Math.PI * eu),
              ep = i
                ? null
                : l
                  ? Y.current
                  : null != (T = x.current)
                    ? T
                    : Y.current,
              ev = W.current;
            (y.current &&
              (y.current.style.opacity = String(c.cj9.smoothstep(ec, 0, 0.86))),
              J.forEach((t, n) => {
                var r;
                let i = B.current[n];
                if (!i) return;
                let a = t.x + t.copy * Q - eo,
                  o = -(0.48 * N.height) + t.height / 2,
                  u =
                    (null == ev ? void 0 : ev.index) === t.index &&
                    ev.copy === t.copy,
                  s =
                    !l &&
                    !R &&
                    (null == ep ? void 0 : ep.index) === t.index &&
                    ep.copy === t.copy,
                  d = c.cj9.damp(
                    null != (r = X.current[n]) ? r : 0,
                    +!!s,
                    5.5,
                    el,
                  );
                X.current[n] = d;
                let v = Math.abs(a) < N.width / 2 + t.width / 2;
                if (((i.visible = u || v), !i.visible)) return;
                let h = i.material.uniforms,
                  m = h.uPointer.value,
                  f = h.uMotion.value;
                if (u && l) {
                  let e = A[l.index],
                    t = Math.max(0, e.length - 1),
                    n = c.cj9.clamp(b.current.value, 0, e.length),
                    r = M.current,
                    i = r ? r.from : Math.min(Math.floor(n), t),
                    a = r ? r.to : n > t ? 0 : Math.min(i + 1, t),
                    o = r ? r.progress : n - i,
                    u = (e) => {
                      if ("image" === e.kind) return L.get(e.src);
                      let t = V.current;
                      if (t && t.readyState >= 2 && $.current) return $.current;
                      let n = E[l.index].at(-1);
                      return L.get(n);
                    },
                    s = u(e[i]),
                    d = u(e[a]);
                  (s &&
                    d &&
                    ((h.uTexture.value = s),
                    (h.uNextTexture.value = d),
                    (h.uMorph.value = o)),
                    (h.uCoverReturn.value = j.current.value));
                } else {
                  let e = z[t.index];
                  ((h.uTexture.value = e),
                    (h.uNextTexture.value = e),
                    (h.uMorph.value = 0),
                    (h.uCoverReturn.value = 0),
                    h.uUvFromScale.value.set(1, 1),
                    h.uUvFromOffset.value.set(0, 0),
                    h.uUvToScale.value.set(1, 1),
                    h.uUvToOffset.value.set(0, 0),
                    h.uUvCoverScale.value.set(1, 1),
                    h.uUvCoverOffset.value.set(0, 0));
                }
                if (u && l && G.current) {
                  let e = G.current,
                    n = t.width / t.height,
                    r = (e) => {
                      let t = Math.min(
                        Math.min(N.width * (R ? 0.86 : 0.48), 1.25 * N.height),
                        N.height * (R ? 0.62 : 0.72) * e,
                      );
                      return { width: t, height: t / e };
                    },
                    u = r(n),
                    s =
                      (t.width * e.scale.x * S.position.z) /
                      Math.max(1, S.position.z - e.position.z);
                  ((u.width = Math.max(u.width, 1.03 * s)),
                    (u.height = u.width / n));
                  let d = A[l.index],
                    v = Math.max(0, d.length - 1),
                    x = c.cj9.clamp(b.current.value, 0, d.length),
                    g = M.current,
                    y = g ? g.from : Math.min(Math.floor(x), v),
                    T = g ? g.to : x > v ? 0 : Math.min(y + 1, v),
                    P = p(g ? g.progress : x - y),
                    C = (e) => {
                      if (0 === e) return u;
                      let t = d[e];
                      if ("video" === t.kind) {
                        let e = V.current;
                        return r(
                          (null == e ? void 0 : e.videoWidth) &&
                            (null == e ? void 0 : e.videoHeight)
                            ? e.videoWidth / e.videoHeight
                            : n,
                        );
                      }
                      let i = L.get(t.src),
                        l = null == i ? void 0 : i.image;
                      return r(
                        (null == l ? void 0 : l.width) &&
                          (null == l ? void 0 : l.height)
                          ? l.width / l.height
                          : n,
                      );
                    },
                    k = C(y),
                    I = C(T),
                    E = c.cj9.lerp(k.width, I.width, P),
                    O = c.cj9.lerp(k.height, I.height, P),
                    U = j.current.value,
                    z = c.cj9.lerp(E, u.width, U),
                    B = c.cj9.lerp(O, u.height, U),
                    D = Math.min(0.14 * N.height, 0.12 * S.position.z),
                    H = (S.position.z - D) / S.position.z,
                    F = (z * H) / t.width,
                    W = (B * H) / t.height,
                    Y = R ? -(0.025 * N.height) * H : 0,
                    X = w.current ? p((0.35 - eu) / 0.35) : 0,
                    _ = 1 - X;
                  (i.position.set(
                    c.cj9.lerp(c.cj9.lerp(e.position.x, 0, ec), a, X),
                    c.cj9.lerp(c.cj9.lerp(e.position.y, Y, ec), o, X),
                    c.cj9.lerp(c.cj9.lerp(e.position.z, D, ec), 0, X),
                  ),
                    i.scale.set(
                      c.cj9.lerp(c.cj9.lerp(e.scale.x, F, ec), 1, X),
                      c.cj9.lerp(c.cj9.lerp(e.scale.y, W, ec), 1, X),
                      c.cj9.lerp(e.scale.z, 1, X),
                    ),
                    i.rotation.set(
                      c.cj9.lerp(e.rotation.x, 0, ec) * _,
                      c.cj9.lerp(e.rotation.y, 0, ec) * _,
                      c.cj9.lerp(e.rotation.z, 0, ec) * _,
                    ),
                    (h.uHover.value = e.hover * (1 - ec) * _),
                    m.copy(e.pointer).multiplyScalar((1 - ec) * _),
                    f.copy(e.motion).multiplyScalar((1 - ec) * _),
                    (h.uTransitionBend.value = 0.8 * ed * _),
                    (h.uEdgeBend.value =
                      (e.edgeBend * (1 - ec) + 6 * ed * h.uWorldScale.value) *
                      _),
                    (h.uOpacity.value = 1),
                    (i.renderOrder = 300));
                } else
                  ((h.uTransitionBend.value = 0),
                    i.position.set(a, o, 0),
                    i.scale.set(1, 1, 1),
                    i.rotation.set(0, 0, 0),
                    (h.uHover.value = 0),
                    m.set(0, 0),
                    f.set(0, 0),
                    (h.uEdgeBend.value = 0),
                    (h.uOpacity.value = 1),
                    (i.renderOrder = n + 1));
                let x = l || R || !ep || s ? 0 : 1;
                if (
                  ((h.uBlur.value = l
                    ? 0
                    : c.cj9.damp(h.uBlur.value, x, 7, el)),
                  u && l)
                ) {
                  let e = Math.max(
                      0.001,
                      (t.width * i.scale.x) / (t.height * i.scale.y),
                    ),
                    n = (t, n, r) => {
                      let i = t.image,
                        l =
                          (null == i ? void 0 : i.videoWidth) ||
                          (null == i ? void 0 : i.width),
                        a =
                          (null == i ? void 0 : i.videoHeight) ||
                          (null == i ? void 0 : i.height),
                        o = l && a ? l / a : e;
                      o > e
                        ? (n.set(e / o, 1), r.set((1 - n.x) / 2, 0))
                        : (n.set(1, o / e), r.set(0, (1 - n.y) / 2));
                    };
                  (n(
                    h.uTexture.value,
                    h.uUvFromScale.value,
                    h.uUvFromOffset.value,
                  ),
                    n(
                      h.uNextTexture.value,
                      h.uUvToScale.value,
                      h.uUvToOffset.value,
                    ),
                    n(
                      h.uCoverTexture.value,
                      h.uUvCoverScale.value,
                      h.uUvCoverOffset.value,
                    ));
                }
                h.uTime.value = e.clock.elapsedTime;
              }),
              l &&
                y.current &&
                (q.current =
                  null !=
                  (Z = (function (e) {
                    let {
                        selected: t,
                        planes: n,
                        meshes: r,
                        imageHeight: i,
                        camera: l,
                        gl: a,
                        size: o,
                        backdrop: u,
                        point: s,
                      } = e,
                      d = n.findIndex(
                        (e) => e.index === t.index && e.copy === t.copy,
                      ),
                      p = r[d],
                      v = n[d];
                    if (p && v) {
                      p.updateWorldMatrix(!0, !1);
                      let e = p.material.uniforms,
                        t = e.uPointer.value,
                        n = e.uMotion.value,
                        r = e.uWorldScale.value,
                        d = e.uEdgeBend.value,
                        h = e.uTransitionBend.value,
                        m = e.uMorph.value,
                        f = e.uEdgeMorphStrength.value,
                        x = e.uHover.value,
                        g = e.uTime.value,
                        w = a.domElement.getBoundingClientRect(),
                        y = [],
                        b = [],
                        M = (a, u) => {
                          let M = Math.sin(a * Math.PI),
                            j = Math.sin(u * Math.PI),
                            T = 2 * a - 1,
                            P = Math.pow(Math.abs(T), 1.4),
                            C = 0.85 + 0.15 * Math.cos((u - 0.5) * Math.PI),
                            k = Math.sin(7 * a - 1.8 * g);
                          (s.set((a - 0.5) * v.width, (u - 0.5) * i, 0),
                            (s.z +=
                              M *
                              j *
                              (0.32 * t.x +
                                0.16 * t.y +
                                k * x * 0.13 +
                                0.29 * n.x +
                                0.24 * n.y) *
                              r),
                            (s.x += j * (0.085 * t.x + 0.085 * n.x) * r),
                            (s.y -= M * (0.065 * t.y - 0.075 * n.y) * r),
                            (s.z += d * (0.56 * P + T * P * 0.17) * C),
                            (s.x += d * T * P * 0.11),
                            (s.y += d * T * (u - 0.5) * 0.07),
                            (s.x +=
                              h * Math.sin(u * Math.PI) * 0.035 * v.width),
                            (s.y +=
                              h *
                              Math.sin(a * Math.PI) *
                              (u - 0.5) *
                              0.035 *
                              v.width),
                            (s.z += h * M * j * 0.16 * r));
                          let S = c.cj9.clamp(e.uCoverReturn.value, 0, 1),
                            N = Math.max(
                              Math.sin(Math.PI * c.cj9.clamp(m, 0, 1)) *
                                (1 - S),
                              Math.sin(Math.PI * S),
                            );
                          ((s.z +=
                            M *
                            j *
                            N *
                            r *
                            (0.38 + 0.22 * Math.sin(7 * a + 3 * u + 0.4 * g))),
                            (s.x += M * j * N * r * 0.075 * Math.sin(8 * u)));
                          let I = 2 * u - 1,
                            R = Math.pow(Math.abs(T), 2.6),
                            E = Math.pow(Math.abs(I), 2.6),
                            A =
                              (Math.sin(2 * u * Math.PI + 0.5 * g + 0.6) +
                                0.3 * Math.sin(4 * u * Math.PI - 0.32 * g)) *
                              Math.sin(u * Math.PI),
                            O =
                              (Math.sin(2 * a * Math.PI - 0.4 * g + 1.2) +
                                0.3 * Math.sin(4 * a * Math.PI + 0.3 * g)) *
                              Math.sin(a * Math.PI),
                            U = N * r * f;
                          ((s.x += T * R * A * U),
                            (s.y += I * E * O * U * 0.68),
                            (s.z +=
                              (R * Math.sin(u * Math.PI) +
                                E * Math.sin(a * Math.PI)) *
                              U *
                              0.65),
                            p.localToWorld(s),
                            s.project(l));
                          let L = w.left + (s.x + 1) * o.width * 0.5,
                            z = w.top + (1 - s.y) * o.height * 0.5;
                          (y.push(
                            ""
                              .concat(L.toFixed(2), "px ")
                              .concat(z.toFixed(2), "px"),
                          ),
                            b.push(L, z));
                        };
                      for (let e = 0; e <= 24; e++) M(e / 24, 0);
                      for (let e = 1; e <= 24; e++) M(1, e / 24);
                      for (let e = 1; e <= 24; e++) M(1 - e / 24, 1);
                      for (let e = 1; e <= 24; e++) M(0, 1 - e / 24);
                      let j = window.innerWidth,
                        T = window.innerHeight;
                      return (
                        (u.style.clipPath = "polygon(evenodd, 0px 0px, "
                          .concat(j, "px 0px, ")
                          .concat(j, "px ")
                          .concat(T, "px, 0px ")
                          .concat(T, "px, 0px 0px, ")
                          .concat(y.join(", "), ")")),
                        b
                      );
                    }
                  })({
                    selected: l,
                    planes: J,
                    meshes: B.current,
                    imageHeight:
                      null !=
                      (U =
                        null ==
                        (O = J.find(
                          (e) => e.index === l.index && e.copy === l.copy,
                        ))
                          ? void 0
                          : O.height)
                        ? U
                        : N.height * (R ? 0.13 : 0.15),
                    camera: S,
                    gl: I,
                    size: N,
                    backdrop: y.current,
                    point: _.current,
                  }))
                    ? Z
                    : []),
              l || (q.current = []));
            let eh = g.current;
            if (eh) {
              let n = eh.querySelector("[data-project-title-text]");
              if (l && G.current) {
                let e = G.current.title,
                  r =
                    (null == (et = t[l.index]) || null == (ee = et.title)
                      ? void 0
                      : ee.trim()) || "Untitled";
                (n && n.textContent !== r && (n.textContent = r),
                  (eh.style.left = "".concat(e.x, "px")),
                  (eh.style.top = "".concat(e.y, "px")),
                  (eh.style.width = "".concat(e.width, "px")),
                  (eh.style.fontSize = "".concat(e.font, "px")),
                  (eh.style.transformOrigin = "left center"),
                  (eh.style.transform =
                    "translateY(-50%) perspective(900px) rotateY("
                      .concat(e.yaw, "rad) rotateX(")
                      .concat(e.pitch, "rad)")),
                  (eh.style.opacity = String(
                    w.current
                      ? 0
                      : c.cj9.smoothstep(G.current.hover, 0.015, 0.42) *
                          (1 - c.cj9.smoothstep(eu, 0, 0.24)),
                  )));
              } else if (l || R) eh.style.opacity = "0";
              else {
                let r = Y.current,
                  i = r
                    ? J.findIndex(
                        (e) => e.index === r.index && e.copy === r.copy,
                      )
                    : -1,
                  l = i >= 0 && null != (en = X.current[i]) ? en : 0;
                if (i >= 0 && l > 0.015) {
                  let r = J[i],
                    a = B.current[i];
                  if (a) {
                    let i = v(a, e.camera, N, r.width, r.height),
                      o =
                        (null == (ei = t[r.index]) || null == (er = ei.title)
                          ? void 0
                          : er.trim()) || "Untitled";
                    (n && n.textContent !== o && (n.textContent = o),
                      (eh.style.left = "".concat(i.x, "px")),
                      (eh.style.top = "".concat(i.y, "px")),
                      (eh.style.width = "".concat(i.width, "px")),
                      (eh.style.fontSize = "".concat(i.font, "px")),
                      (eh.style.transformOrigin = "left center"),
                      (eh.style.transform =
                        "translateY(-50%) perspective(900px) rotateY("
                          .concat(i.yaw, "rad) rotateX(")
                          .concat(i.pitch, "rad)")),
                      (eh.style.opacity = String(
                        c.cj9.smoothstep(l, 0.015, 0.42),
                      )));
                  } else eh.style.opacity = "0";
                } else eh.style.opacity = "0";
              }
            }
            F.current = !0;
          }),
          (0, r.jsx)("group", {
            children: J.map((e, t) =>
              (0, r.jsxs)(
                "mesh",
                {
                  ref: (e) => {
                    B.current[t] = e;
                  },
                  frustumCulled: !1,
                  children: [
                    (0, r.jsx)("planeGeometry", {
                      args: [e.width, e.height, 64, 88],
                    }),
                    (0, r.jsx)("shaderMaterial", {
                      uniforms: Z[t],
                      vertexShader:
                        "\n  uniform float uTime, uHover, uWorldScale, uEdgeBend, uTransitionBend, uMorph, uCoverReturn, uEdgeMorphStrength;\n  uniform vec2 uPointer, uMotion, uImageSize;\n  varying vec2 vUv;\n\n  const float PI = 3.14159265359;\n\n  void main() {\n    vUv = uv;\n\n    vec3 p = position;\n    vec2 q = p.xy / uImageSize + 0.5;\n\n    float sx = sin(q.x * PI);\n    float sy = sin(q.y * PI);\n    float wave = sin(q.x * 7.0 - uTime * 1.8);\n\n    p.z += sx * sy * (\n      uPointer.x * 0.32 + uPointer.y * 0.16 +\n      wave * uHover * 0.13 +\n      uMotion.x * 0.29 + uMotion.y * 0.24\n    ) * uWorldScale;\n\n    p.x += sy * (\n      uPointer.x * 0.085 + uMotion.x * 0.085\n    ) * uWorldScale;\n\n    p.y -= sx * (\n      uPointer.y * 0.065 - uMotion.y * 0.075\n    ) * uWorldScale;\n\n    float side = uv.x * 2.0 - 1.0;\n    float edge = pow(abs(side), 1.4);\n\n    float verticalProfile =\n      0.85 + 0.15 * cos((uv.y - 0.5) * PI);\n\n    p.z += uEdgeBend *\n      (edge * 0.56 + side * edge * 0.17) *\n      verticalProfile;\n\n    p.x += uEdgeBend * side * edge * 0.11;\n\n    p.y += uEdgeBend * side *\n      (uv.y - 0.5) * 0.07;\n\n    p.x += uTransitionBend *\n      sin(uv.y * PI) * 0.035 * uImageSize.x;\n\n    p.y += uTransitionBend *\n      sin(uv.x * PI) *\n      (uv.y - 0.5) * 0.035 * uImageSize.x;\n\n    p.z += uTransitionBend *\n      sin(uv.x * PI) *\n      sin(uv.y * PI) *\n      0.16 * uWorldScale;\n\n    float morphPulse = max(\n      sin(PI * uMorph) * (1.0 - uCoverReturn),\n      sin(PI * uCoverReturn)\n    );\n\n    p.z += sx * sy * morphPulse * uWorldScale *\n      (\n        0.38 + 0.22 *\n        sin(\n          uv.x * 7.0 +\n          uv.y * 3.0 +\n          uTime * 0.4\n        )\n      );\n\n    p.x += sx * sy * morphPulse *\n      uWorldScale * 0.075 *\n      sin(uv.y * 8.0);\n\n    float verticalSide = uv.y * 2.0 - 1.0;\n\n    float sideMask = pow(abs(side), 2.6);\n    float topBottomMask = pow(abs(verticalSide), 2.6);\n\n    float sideFlow = (\n      sin(uv.y * 6.2831853 + uTime * 0.5 + 0.6) +\n      0.3 * sin(uv.y * 12.5663706 - uTime * 0.32)\n    ) * sin(uv.y * PI);\n\n    float topBottomFlow = (\n      sin(uv.x * 6.2831853 - uTime * 0.4 + 1.2) +\n      0.3 * sin(uv.x * 12.5663706 + uTime * 0.3)\n    ) * sin(uv.x * PI);\n\n    float edgeAmount =\n      morphPulse * uWorldScale * uEdgeMorphStrength;\n\n    p.x += side * sideMask *\n      sideFlow * edgeAmount;\n\n    p.y += verticalSide *\n      topBottomMask *\n      topBottomFlow *\n      edgeAmount * 0.68;\n\n    p.z += (\n      sideMask * sin(uv.y * PI) +\n      topBottomMask * sin(uv.x * PI)\n    ) * edgeAmount * 0.65;\n\n    gl_Position =\n      projectionMatrix *\n      modelViewMatrix *\n      vec4(p, 1.0);\n  }\n",
                      fragmentShader: d,
                      transparent: !0,
                      depthTest: !1,
                      depthWrite: !1,
                      toneMapped: !1,
                      side: c.$EB,
                    }),
                  ],
                },
                "".concat(e.index, "-").concat(e.copy),
              ),
            ),
          })
        );
      }
      function x() {
        let { camera: e, size: t } = (0, u.A)();
        return (
          (0, o.useLayoutEffect)(() => {
            if (!(e instanceof c.ubm)) return;
            let n = c.cj9.degToRad(e.fov / 2);
            (e.position.set(0, 0, t.height / (2 * Math.tan(n))),
              (e.aspect = t.width / t.height),
              (e.far = 2e4),
              e.updateProjectionMatrix(),
              e.updateMatrixWorld(!0));
          }, [e, t.width, t.height]),
          null
        );
      }
      function g(e) {
        let { backdropRef: t } = e;
        return (0, r.jsx)("div", {
          ref: (e) => {
            t.current = e;
          },
          "aria-hidden": "true",
          className:
            "pointer-events-none fixed inset-0 z-[15] bg-[#0e0d0c]/97 backdrop-blur-[24px] opacity-0",
        });
      }
      function w(e) {
        let { titleRef: t, title: n } = e;
        return (0, r.jsx)("div", {
          ref: (e) => {
            t.current = e;
          },
          "aria-hidden": "true",
          className:
            "pointer-events-none absolute left-0 top-0 z-[40] max-w-[90vw] break-words font-bueno font-bold uppercase leading-[1.02] tracking-[0.005em] text-white mix-blend-difference",
          style: { opacity: 0, willChange: "left, top, transform, opacity" },
          children: (0, r.jsx)("span", {
            className: "block overflow-hidden",
            children: (0, r.jsx)("span", {
              "data-project-title-text": !0,
              className: "block will-change-transform",
              children: n,
            }),
          }),
        });
      }
      var y = n(6799),
        b = n(3084),
        M = n(9400);
      let j = {
          hidden: {},
          visible: { transition: { delayChildren: 0, staggerChildren: 0.035 } },
          exit: { opacity: 0, transition: { duration: 0.25, ease: "easeOut" } },
        },
        T = { hidden: {}, visible: { transition: { staggerChildren: 0.025 } } },
        P = {
          hidden: { y: "115%", opacity: 0, filter: "blur(3px)" },
          visible: {
            y: "0%",
            opacity: 1,
            filter: "blur(0px)",
            transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] },
          },
        },
        C = {
          hidden: { opacity: 0 },
          visible: { opacity: 1, transition: { duration: 0.2 } },
        };
      function k(e) {
        var t;
        let {
            text: n,
            delay: i = 0,
            stagger: l = 0.015,
            reducedMotion: a = !1,
          } = e,
          o = null != (t = n.match(/\S+|\s+/g)) ? t : [];
        return (0, r.jsx)(y.P.span, {
          className: "block whitespace-pre-line",
          variants: {
            hidden: {},
            visible: {
              transition: {
                delayChildren: a ? 0 : i,
                staggerChildren: a ? 0 : l,
              },
            },
          },
          children: o.map((e, t) =>
            /^\s+$/.test(e)
              ? (0, r.jsx)("span", { children: e }, t)
              : (0, r.jsx)(
                  "span",
                  {
                    className:
                      "inline-block overflow-hidden align-bottom pb-[0.12em] -mb-[0.12em]",
                    children: (0, r.jsx)(y.P.span, {
                      className: "inline-block will-change-transform",
                      variants: a ? C : P,
                      children: e,
                    }),
                  },
                  t,
                ),
          ),
        });
      }
      function S(e) {
        let {
          label: t,
          value: n,
          labelClassName: i,
          valueClassName: l,
          reducedMotion: a,
        } = e;
        return (0, r.jsxs)(y.P.div, {
          variants: T,
          children: [
            (0, r.jsx)("p", {
              className: i,
              children: (0, r.jsx)(k, {
                text: t,
                stagger: 0,
                reducedMotion: a,
              }),
            }),
            (0, r.jsx)("p", {
              className: l,
              children: (0, r.jsx)(k, { text: n, reducedMotion: a }),
            }),
          ],
        });
      }
      function N(e) {
        var t, n, i, l, a, o, u, s, c, d, p, v;
        let {
            selected: h,
            closing: m,
            ready: f,
            project: x,
            currentMediaIndex: g,
            mediaCount: w,
            onSelectMedia: N,
            onMenuHoverChange: I,
          } = e,
          R = null != (v = (0, b.I)()) && v;
        return (0, r.jsx)(M.N, {
          children:
            h &&
            !m &&
            f &&
            x &&
            (0, r.jsxs)(
              y.P.div,
              {
                initial: "hidden",
                animate: "visible",
                exit: "exit",
                variants: j,
                className:
                  "pointer-events-none absolute inset-0 z-20 text-[#e7e3dd]",
                children: [
                  (0, r.jsxs)(y.P.div, {
                    variants: T,
                    className:
                      "absolute left-[5%] top-[7%] z-30 w-[88%] md:left-[3.5%] md:top-[27%] md:w-[20.5%]",
                    children: [
                      (0, r.jsx)("h2", {
                        className:
                          "break-words font-bueno text-[clamp(21px,4.5vw,28px)] font-bold uppercase leading-[1.08] tracking-[-0.012em] text-[#e7e3dd] md:text-[clamp(22px,1.45vw,27px)]",
                        children: (0, r.jsx)(k, {
                          text:
                            (null == (t = x.title) ? void 0 : t.trim()) ||
                            "Untitled",
                          stagger: 0.025,
                          reducedMotion: R,
                        }),
                      }),
                      (null == (n = x.description) ? void 0 : n.trim()) &&
                        (0, r.jsx)(y.P.div, {
                          variants: T,
                          className:
                            " mt-8 hidden md:block lg:mt-11  [@media(max-height:800px)]:!mt-6 [@media(max-height:650px)]:!mt-4 ",
                          children: (0, r.jsx)("p", {
                            className:
                              " whitespace-pre-line break-words font-bueno text-[clamp(15px,1.05vw,18px)] leading-[1.55] text-[#e7e3dd]/78  [@media(max-height:800px)]:text-[15px] [@media(max-height:800px)]:leading-[1.45]  [@media(max-height:650px)]:text-[14px] [@media(max-height:650px)]:leading-[1.4] ",
                            children: (0, r.jsx)(k, {
                              text: x.description,
                              reducedMotion: R,
                            }),
                          }),
                        }),
                    ],
                  }),
                  (null == (i = x.description) ? void 0 : i.trim()) &&
                    (0, r.jsx)(y.P.div, {
                      variants: T,
                      className:
                        "absolute bottom-[28%] left-[5%] right-[5%] md:hidden",
                      children: (0, r.jsx)(S, {
                        label: "Description",
                        value: x.description,
                        reducedMotion: R,
                        labelClassName:
                          "mb-2 font-sans text-[9px] font-medium uppercase tracking-[0.2em] text-[#e7e3dd]/45",
                        valueClassName:
                          "line-clamp-3 whitespace-pre-line break-words font-bueno text-[13px] leading-[1.38] text-[#e7e3dd]/85",
                      }),
                    }),
                  ((null == (l = x.type) ? void 0 : l.trim()) ||
                    (null == (a = x.tools) ? void 0 : a.trim())) &&
                    (0, r.jsxs)("div", {
                      className:
                        "absolute bottom-[26%] right-[3.8%] hidden w-[18.5%] flex-col items-start gap-6 md:flex",
                      children: [
                        (null == (o = x.type) ? void 0 : o.trim()) &&
                          (0, r.jsx)(S, {
                            label: "Year:",
                            value: x.type,
                            reducedMotion: R,
                            labelClassName:
                              "mb-3 font-sans text-[10px] font-medium  tracking-[0.18em] text-[#e7e3dd]",
                            valueClassName:
                              "break-words font-bueno text-[clamp(16px,1.1vw,19px)] font-medium leading-[1.3] text-[#e7e3dd]/90",
                          }),
                        (null == (u = x.tools) ? void 0 : u.trim()) &&
                          (0, r.jsx)(S, {
                            label: "Tools:",
                            value: x.tools,
                            reducedMotion: R,
                            labelClassName:
                              "mb-3 font-sans text-[10px] font-medium  tracking-[0.18em] text-[#e7e3dd]",
                            valueClassName:
                              "whitespace-pre-line break-words font-bueno text-[clamp(16px,1.1vw,19px)] font-medium leading-[1.3] text-[#e7e3dd]/90",
                          }),
                      ],
                    }),
                  ((null == (s = x.type) ? void 0 : s.trim()) ||
                    (null == (c = x.tools) ? void 0 : c.trim())) &&
                    (0, r.jsxs)("div", {
                      className:
                        "absolute bottom-[10%] left-[5%] right-[5%] flex flex-col items-start gap-3 md:hidden",
                      children: [
                        (null == (d = x.type) ? void 0 : d.trim()) &&
                          (0, r.jsx)(S, {
                            label: "Year",
                            value: x.type,
                            reducedMotion: R,
                            labelClassName:
                              "mb-1 text-[9px] uppercase tracking-[0.2em] text-[#e7e3dd]/55",
                            valueClassName:
                              "break-words font-bueno text-[12px] leading-[1.25]",
                          }),
                        (null == (p = x.tools) ? void 0 : p.trim()) &&
                          (0, r.jsx)(S, {
                            label: "Tools",
                            value: x.tools,
                            reducedMotion: R,
                            labelClassName:
                              "mb-1 text-[9px] uppercase tracking-[0.2em] text-[#e7e3dd]/55",
                            valueClassName:
                              "line-clamp-2 break-words font-bueno text-[12px] leading-[1.25]",
                          }),
                      ],
                    }),
                  (0, r.jsxs)(y.P.div, {
                    variants: T,
                    className:
                      "absolute bottom-[3.5%] left-[5%] right-[5%] grid grid-cols-[minmax(0,1fr)_minmax(0,1fr)_minmax(0,1fr)] items-end gap-2 md:bottom-[5%] md:left-[5.3%] md:right-[4%]",
                    children: [
                      (0, r.jsx)("div", {
                        className: "min-w-0 overflow-hidden",
                        children: (0, r.jsx)(y.P.p, {
                          variants: R ? C : P,
                          className:
                            "text-[9px] font-medium uppercase leading-[1.4] tracking-[0.16em] text-[#e7e3dd]/80 md:text-[10px]",
                          children: "Scroll or click to explore",
                        }),
                      }),
                      (0, r.jsx)("div", {
                        className: "min-w-0 overflow-hidden text-center",
                        children:
                          x.tags.length > 0 &&
                          (0, r.jsx)(y.P.p, {
                            variants: R ? C : P,
                            className:
                              "truncate whitespace-nowrap font-sans text-[8px] font-medium uppercase leading-[1.4] tracking-[0.12em] text-[#e7e3dd]/80 md:text-[10px] md:tracking-[0.16em]",
                            title: x.tags.join(" / "),
                            children: x.tags
                              .filter((e) => e.trim().length > 0)
                              .join(" / "),
                          }),
                      }),
                      (0, r.jsx)("nav", {
                        "aria-label": "Project media navigation",
                        className:
                          "pointer-events-auto flex w-max max-w-full min-w-0 justify-self-end items-center justify-end gap-[clamp(9px,1.2vw,20px)] overflow-x-auto whitespace-nowrap font-bueno text-[clamp(15px,1.15vw,19px)] font-medium tabular-nums [scrollbar-width:none] [&::-webkit-scrollbar]:hidden",
                        onPointerEnter: (e) => {
                          "mouse" === e.pointerType && I(!0);
                        },
                        onPointerLeave: () => I(!1),
                        onFocus: () => I(!0),
                        onBlur: (e) => {
                          e.currentTarget.contains(e.relatedTarget) || I(!1);
                        },
                        children: Array.from({ length: w }, (e, t) =>
                          (0, r.jsx)(
                            "button",
                            {
                              type: "button",
                              "aria-label": "Show project media ".concat(t + 1),
                              "aria-current": t === g ? "true" : void 0,
                              onClick: () => N(t),
                              className:
                                "shrink-0 border-0 bg-transparent px-1 py-2 leading-none outline-offset-4 transition-opacity duration-300 ease-in-out focus-visible:outline focus-visible:outline-1 focus-visible:outline-[#e7e3dd] ".concat(
                                  g === t
                                    ? "text-[#e7e3dd] opacity-100"
                                    : "text-[#e7e3dd] opacity-30 hover:opacity-100",
                                ),
                              children: t + 1,
                            },
                            t,
                          ),
                        ),
                      }),
                    ],
                  }),
                ],
              },
              "details-".concat(x.id, "-").concat(h.copy),
            ),
        });
      }
      function I(e) {
        let {
            active: t,
            hasMultipleMedia: n,
            isOverImage: i,
            initialMousePosition: l,
            menuHovered: u = !1,
          } = e,
          s = (0, o.useRef)(null),
          c = (0, o.useRef)(null),
          d = (0, o.useRef)(null),
          p = (0, o.useRef)(null),
          v = (0, o.useRef)(null),
          [h, m] = (0, o.useState)("RETURN"),
          f = (0, o.useRef)({ hasMultipleMedia: n, isOverImage: i });
        return (
          (f.current = { hasMultipleMedia: n, isOverImage: i }),
          (0, o.useEffect)(() => {
            let e = p.current;
            if (e && t && !u)
              return (
                a.Ay.fromTo(
                  e,
                  { y: 7, autoAlpha: 0 },
                  {
                    y: 0,
                    autoAlpha: 1,
                    duration: 0.42,
                    ease: "expo.out",
                    overwrite: !0,
                  },
                ),
                () => {
                  a.Ay.killTweensOf(e);
                }
              );
          }, [h, t, u]),
          (0, o.useEffect)(() => {
            let e = p.current,
              n = v.current;
            if (!e || !n || !t) return;
            let r = window.matchMedia(
              "(prefers-reduced-motion: reduce)",
            ).matches;
            return (
              u
                ? (a.Ay.to(e, {
                    autoAlpha: 0,
                    scale: 0.75,
                    y: 0,
                    duration: 0.22 * !r,
                    ease: "power2.inOut",
                    overwrite: !0,
                  }),
                  a.Ay.to(n, {
                    autoAlpha: 1,
                    scale: 1,
                    duration: 0.3 * !r,
                    delay: 0.04 * !r,
                    ease: "power3.out",
                    overwrite: !0,
                  }))
                : (a.Ay.to(n, {
                    autoAlpha: 0,
                    scale: 0.35,
                    duration: 0.22 * !r,
                    ease: "power2.inOut",
                    overwrite: !0,
                  }),
                  a.Ay.to(e, {
                    autoAlpha: 1,
                    scale: 1,
                    y: 0,
                    duration: 0.38 * !r,
                    delay: 0.04 * !r,
                    ease: "expo.out",
                    overwrite: !0,
                  })),
              () => {
                (a.Ay.killTweensOf(e), a.Ay.killTweensOf(n));
              }
            );
          }, [u, t]),
          (0, o.useEffect)(() => {
            if (!t) return;
            let e = s.current,
              n = c.current,
              r = d.current,
              i = p.current;
            if (
              !e ||
              !n ||
              !r ||
              !i ||
              !window.matchMedia("(hover: hover) and (pointer: fine)").matches
            )
              return;
            let o = window.matchMedia(
                "(prefers-reduced-motion: reduce)",
              ).matches,
              u = e.closest("section");
            (null == u || u.classList.add("project-kinetic-cursor-active"),
              a.Ay.set(e, { autoAlpha: 0 }));
            let v = !1,
              h = !1,
              x = 0,
              g = 0,
              w = 0,
              y = 0,
              b = 0,
              M = 0,
              j = 0,
              T = 0,
              P = null,
              C = () => {
                var e, t;
                if (!v) return;
                let n =
                  f.current.hasMultipleMedia &&
                  (null == (e = (t = f.current.isOverImage).current)
                    ? void 0
                    : e.call(t, x, g))
                    ? "NEXT"
                    : "RETURN";
                n !== P && ((P = n), m(n));
              },
              k = (t) => {
                j = 0;
                let r = T ? Math.max(1, Math.min(50, t - T)) : 1e3 / 60;
                T = t;
                let l = r / 1e3,
                  a = o ? 1 : 1 - Math.exp(-10 * l),
                  u = w,
                  s = y;
                ((w += (x - w) * a), (y += (g - y) * a));
                let c = (w - u) / 60 / l,
                  d = (y - s) / 60 / l,
                  p = Math.hypot(c, d),
                  v = o ? 0 : Math.min(p / 15, 1),
                  m = o
                    ? 0
                    : Math.max(-2.5, Math.min(2.5, 0.22 * c + 0.04 * d)),
                  f = o ? 1 : 1 - Math.exp(-11 * l);
                ((b += (m - b) * f), (M += (0.35 * v - M) * f));
                let P = 0.1 > Math.abs(x - w) && 0.1 > Math.abs(g - y),
                  S = 0.015 > Math.abs(b) && 3e-4 > Math.abs(M);
                (P && ((w = x), (y = g)),
                  S && p < 0.05 && ((b = 0), (M = 0)),
                  (e.style.transform = "translate3d("
                    .concat(w, "px, ")
                    .concat(y, "px, 0)")),
                  (n.style.transform = "rotate(".concat(b, "deg)")),
                  (i.style.letterSpacing = "".concat(0.11 + M, "em")),
                  C(),
                  !h || (P && S)
                    ? (T = 0)
                    : (j = window.requestAnimationFrame(k)));
              },
              S = () => {
                j || (j = window.requestAnimationFrame(k));
              },
              N = () => {
                !h &&
                  v &&
                  ((h = !0),
                  a.Ay.to(e, {
                    autoAlpha: 1,
                    duration: 0.3 * !o,
                    ease: "power2.out",
                    overwrite: !0,
                  }));
              },
              I = () => {
                h &&
                  ((h = !1),
                  a.Ay.to(e, {
                    autoAlpha: 0,
                    duration: 0.2 * !o,
                    ease: "power2.out",
                    overwrite: !0,
                  }));
              },
              R = (t, n) => {
                ((x = t),
                  (g = n),
                  v ||
                    ((v = !0),
                    (w = t),
                    (y = n),
                    (e.style.transform = "translate3d("
                      .concat(t, "px, ")
                      .concat(n, "px, 0)"))),
                  C(),
                  S(),
                  N());
              },
              E = (e) => {
                e.isPrimary &&
                  "touch" !== e.pointerType &&
                  R(e.clientX, e.clientY);
              },
              A = (e) => {
                R(e.clientX, e.clientY);
              },
              O = (e) => {
                e.isPrimary &&
                  "touch" !== e.pointerType &&
                  0 === e.button &&
                  (R(e.clientX, e.clientY),
                  a.Ay.to(r, {
                    scale: 0.82,
                    duration: 0.14 * !o,
                    ease: "power2.out",
                    overwrite: !0,
                  }));
              },
              U = (e) => {
                e.isPrimary &&
                  "touch" !== e.pointerType &&
                  0 === e.button &&
                  a.Ay.to(r, {
                    scale: 1,
                    duration: 0.33 * !o,
                    ease: "expo.out",
                    overwrite: !0,
                  });
              },
              L = () => {
                a.Ay.to(r, {
                  scale: 1,
                  duration: 0.2 * !o,
                  ease: "power2.out",
                  overwrite: !0,
                });
              },
              z = (e) => {
                e.relatedTarget || I();
              };
            (window.addEventListener("pointermove", E, !0),
              window.addEventListener("mousemove", A, !0),
              window.addEventListener("pointerdown", O, !0),
              window.addEventListener("pointerup", U, !0),
              window.addEventListener("pointercancel", L, !0),
              document.addEventListener("mouseout", z, !0),
              window.addEventListener("blur", I));
            let B = l.current;
            B && R(B.x, B.y);
            let D = 0,
              H = () => {
                (C(), (D = window.requestAnimationFrame(H)));
              };
            return (
              (D = window.requestAnimationFrame(H)),
              () => {
                (null == u ||
                  u.classList.remove("project-kinetic-cursor-active"),
                  window.cancelAnimationFrame(j),
                  window.cancelAnimationFrame(D),
                  window.removeEventListener("pointermove", E, !0),
                  window.removeEventListener("mousemove", A, !0),
                  window.removeEventListener("pointerdown", O, !0),
                  window.removeEventListener("pointerup", U, !0),
                  window.removeEventListener("pointercancel", L, !0),
                  document.removeEventListener("mouseout", z, !0),
                  window.removeEventListener("blur", I),
                  a.Ay.killTweensOf(e),
                  a.Ay.killTweensOf(r));
              }
            );
          }, [t, l]),
          (0, r.jsxs)(r.Fragment, {
            children: [
              (0, r.jsx)("style", {
                children:
                  "\n        @media (hover: hover) and (pointer: fine) {\n          .project-kinetic-cursor-active,\n          .project-kinetic-cursor-active * {\n            cursor: none !important;\n          }\n        }\n      ",
              }),
              (0, r.jsx)("div", {
                ref: s,
                "aria-hidden": "true",
                className:
                  "pointer-events-none fixed left-0 top-0 z-[9999] mix-blend-difference opacity-0",
                style: {
                  transform: "translate3d(-200px, -200px, 0)",
                  willChange: "transform, opacity",
                },
                children: (0, r.jsx)("div", {
                  className:
                    "absolute left-0 top-0 -translate-x-1/2 -translate-y-1/2",
                  children: (0, r.jsx)("div", {
                    ref: c,
                    className: "origin-center will-change-transform",
                    children: (0, r.jsxs)("div", {
                      ref: d,
                      className:
                        "relative flex items-center justify-center origin-center will-change-transform",
                      children: [
                        (0, r.jsx)("span", {
                          ref: p,
                          className:
                            "block whitespace-nowrap font-sans text-[14px] font-semibold uppercase leading-none tracking-[0.11em] text-white will-change-transform",
                          children: h,
                        }),
                        (0, r.jsx)("span", {
                          ref: v,
                          className:
                            "pointer-events-none absolute left-1/2 top-1/2 h-[8px] w-[8px] -translate-x-1/2 -translate-y-1/2 bg-white opacity-0",
                          style: {
                            scale: 0.35,
                            willChange: "transform, opacity",
                          },
                        }),
                      ],
                    }),
                  }),
                }),
              }),
            ],
          })
        );
      }
      let R = d
          .replace(
            "varying vec2 vUv;",
            "varying vec2 vUv;\n  varying float vProfileShade;",
          )
          .replace(
            /gl_FragColor\s*=\s*vec4\(\s*color\.rgb\s*,\s*uOpacity\s*\)\s*;/g,
            "gl_FragColor = vec4(color.rgb * vProfileShade, uOpacity);",
          ),
        E = [
          { src: "/rk-portrait.jpg", discipline: null },
          { src: "/visual-identity.jpg", discipline: "Visual Identities" },
          { src: "/logo-design.jpg", discipline: "Logo Design" },
          { src: "/art-direction.jpg", discipline: "Art Direction" },
          { src: "/bylarm-new.mp4", discipline: "Motion & Animation" },
          { src: "/editorial-design.jpg", discipline: "Editorial Design" },
        ],
        A = (e) => /\.(mp4|webm|ogv)(?:\?|$)/i.test(e),
        O = E.filter((e) => !A(e.src)).map((e) => e.src),
        U = E.filter((e) => A(e.src)).map((e) => e.src);
      function L(e) {
        let t =
            arguments.length > 1 && void 0 !== arguments[1]
              ? arguments[1]
              : 0.8,
          n = e.image,
          r =
            (null == n ? void 0 : n.videoWidth) ||
            (null == n ? void 0 : n.width),
          i =
            (null == n ? void 0 : n.videoHeight) ||
            (null == n ? void 0 : n.height);
        return r && i ? r / i : t;
      }
      function z(e, t, n, r) {
        let i = L(e, t);
        i > t
          ? (n.set(t / i, 1), r.set((1 - n.x) / 2, 0))
          : (n.set(1, i / t), r.set(0, (1 - n.y) / 2));
      }
      function B(e) {
        let {
            open: t,
            projectSelected: n,
            mediaProgress: i,
            mediaJump: l,
            coverReturn: d,
            isOverImage: v,
            onReadyChange: h,
            onClosed: m,
            htmlBackdropRef: f,
          } = e,
          { size: x, camera: g, gl: w } = (0, u.A)(),
          y = (0, s.zo)(O),
          b = (0, o.useMemo)(() => new Map(O.map((e, t) => [e, y[t]])), [y]),
          M = (0, o.useRef)(new Map()),
          j = (function (e, t) {
            let n = e < 1024,
              r = n
                ? Math.min(140, Math.max(104, 0.28 * e))
                : Math.min(210, Math.max(150, 0.12 * e)),
              i = r / 0.8;
            return {
              thumbnailWidth: r,
              thumbnailHeight: i,
              thumbnailX: e / 2 - e * (n ? 0.05 : 0.031) - r / 2,
              thumbnailY: t / 2 - (n ? 225 : 150) - i / 2,
              mobile: n,
            };
          })(x.width, x.height),
          T = (0, o.useRef)(null),
          P = (0, o.useRef)(null),
          C = (0, o.useRef)(null),
          k = (0, o.useRef)({ value: 0 }),
          S = (0, o.useRef)(!1),
          N = (0, o.useRef)([]),
          I = (0, o.useMemo)(
            () => ({
              uTexture: { value: y[0] },
              uNextTexture: { value: y[0] },
              uCoverTexture: { value: y[0] },
              uMorph: { value: 0 },
              uCoverReturn: { value: 0 },
              uEdgeMorphStrength: { value: 0.22 },
              uUvFromScale: { value: new c.I9Y(1, 1) },
              uUvFromOffset: { value: new c.I9Y() },
              uUvToScale: { value: new c.I9Y(1, 1) },
              uUvToOffset: { value: new c.I9Y() },
              uUvCoverScale: { value: new c.I9Y(1, 1) },
              uUvCoverOffset: { value: new c.I9Y() },
              uTime: { value: 0 },
              uWorldScale: { value: 1 },
              uImageSize: { value: new c.I9Y(1, 1) },
              uTravelLag: { value: new c.I9Y() },
              uDepthBend: { value: 0 },
              uClosing: { value: 0 },
              uOpacity: { value: 1 },
              uBlur: { value: 0 },
            }),
            [y],
          );
        return (
          (0, o.useEffect)(() => {
            y.forEach((e) => {
              ((e.colorSpace = c.er$),
                (e.anisotropy = 4),
                (e.needsUpdate = !0));
            });
          }, [y]),
          (0, o.useEffect)(() => {
            let e = M.current;
            for (let t of U) {
              let n = document.createElement("video");
              ((n.crossOrigin = "anonymous"),
                (n.muted = !0),
                (n.defaultMuted = !0),
                (n.loop = !0),
                (n.playsInline = !0),
                (n.preload = "auto"),
                (n.src = t),
                n.load());
              let r = new c.Nv2(n);
              ((r.colorSpace = c.er$),
                (r.minFilter = c.k6q),
                (r.magFilter = c.k6q),
                (r.generateMipmaps = !1),
                e.set(t, { video: n, texture: r, requested: !1 }));
            }
            return () => {
              for (let { video: t, texture: n } of e.values())
                (t.pause(), t.removeAttribute("src"), t.load(), n.dispose());
              e.clear();
            };
          }, []),
          (0, o.useEffect)(
            () => (
              (v.current = (e, t) => {
                let n = N.current;
                if (8 !== n.length) return !1;
                let r = !1;
                for (let i = 0, l = 3; i < 4; l = i++) {
                  let a = n[2 * i],
                    o = n[2 * i + 1],
                    u = n[2 * l],
                    s = n[2 * l + 1];
                  o > t != s > t &&
                    e < ((u - a) * (t - o)) / (s - o) + a &&
                    (r = !r);
                }
                return r;
              }),
              () => {
                v.current = null;
              }
            ),
            [v],
          ),
          (0, o.useEffect)(() => {
            if (!t && !S.current) return;
            (t && (S.current = !0), h(!1));
            let e = a.Ay.to(k.current, {
              value: +!!t,
              duration: 0.9,
              ease: "none",
              overwrite: !0,
              onComplete: () => {
                t ? h(!0) : m();
              },
            });
            return () => {
              e.kill();
            };
          }, [t, h, m]),
          (0, u.C)((e) => {
            let r = T.current;
            if (!r) return;
            let a = c.cj9.clamp(k.current.value, 0, 1),
              o = p(a),
              u = c.cj9.clamp(d.current.value, 0, 1),
              s = P.current,
              v = C.current;
            (s && v && (s.visible = !1), (r.visible = !0));
            let h = E.length,
              m = c.cj9.clamp(i.current.value, 0, h),
              S = h - 1,
              R = l.current,
              A = R ? R.from : Math.min(Math.floor(m), S),
              O = R ? R.to : m > S ? 0 : Math.min(A + 1, S),
              U = R ? R.progress : m - A,
              B = p(U);
            for (let [e, r] of M.current)
              t &&
              !n &&
              a > 0.95 &&
              (E[A].src === e || (U > 0.001 && E[O].src === e))
                ? r.video.paused &&
                  !r.requested &&
                  ((r.requested = !0),
                  r.video.play().catch(() => {
                    ((r.requested = !1),
                      console.warn("Could not play profile video: ".concat(e)));
                  }))
                : (r.video.paused || r.video.pause(), (r.requested = !1));
            let D = (e) => {
                let t = E[e].src,
                  n = b.get(t);
                if (n) return n;
                let r = M.current.get(t);
                return r && r.video.readyState >= 2 ? r.texture : y[0];
              },
              H = D(A),
              F = D(O),
              W = (e) => {
                let t = Math.min(
                  Math.min(x.width * (j.mobile ? 0.86 : 0.48), 1.25 * x.height),
                  x.height * (j.mobile ? 0.62 : 0.72) * e,
                );
                return { width: t, height: t / e };
              },
              Y = W(0.8),
              X = W(0 === A ? 0.8 : L(H)),
              G = W(0 === O ? 0.8 : L(F)),
              _ = c.cj9.lerp(X.width, G.width, B),
              q = c.cj9.lerp(X.height, G.height, B),
              V = c.cj9.lerp(_, Y.width, u),
              $ = c.cj9.lerp(q, Y.height, u),
              K = Math.min(0.14 * x.height, 0.12 * g.position.z),
              J = (g.position.z - K) / g.position.z,
              Q = (V * J) / j.thumbnailWidth,
              Z = ($ * J) / j.thumbnailHeight,
              ee = j.mobile ? -(0.025 * x.height) * J : 0;
            (r.position.set(
              c.cj9.lerp(j.thumbnailX, 0, o),
              c.cj9.lerp(j.thumbnailY, ee, o),
              c.cj9.lerp(0, K, o),
            ),
              r.scale.set(
                c.cj9.lerp(1, Q, o),
                c.cj9.lerp(1, Z, o),
                c.cj9.lerp(1, Math.min(Q, Z), o),
              ));
            let et = (6 * a * (1 - a)) / 0.9,
              en = c.cj9.clamp(
                (Math.abs(j.thumbnailX) * et * 0.14) /
                  Math.max(r.scale.x, 0.001),
                0,
                0.35 * j.thumbnailWidth,
              ),
              er = c.cj9.clamp(
                (Math.abs(j.thumbnailY - ee) * et * 0.14) /
                  Math.max(r.scale.y, 0.001),
                0,
                0.28 * j.thumbnailHeight,
              ),
              ei = t ? 1 : -1;
            (I.uTravelLag.value.set(en * ei, er * ei),
              (I.uDepthBend.value = 0.92 * Math.sqrt(en * en + er * er * 0.55)),
              (I.uClosing.value = +!t));
            let el = Math.sin(Math.PI * a);
            (r.rotation.set(0, el * (t ? -0.22 : 0.22), 0),
              (r.renderOrder = n ? 299 : 600),
              (I.uTexture.value = H),
              (I.uNextTexture.value = F),
              (I.uCoverTexture.value = y[0]),
              (I.uMorph.value = U),
              (I.uCoverReturn.value = u),
              (I.uTime.value = e.clock.elapsedTime),
              (I.uWorldScale.value = j.thumbnailHeight / 3.6),
              I.uImageSize.value.set(j.thumbnailWidth, j.thumbnailHeight));
            let ea = Math.max(
              0.001,
              (j.thumbnailWidth * r.scale.x) / (j.thumbnailHeight * r.scale.y),
            );
            (z(H, ea, I.uUvFromScale.value, I.uUvFromOffset.value),
              z(F, ea, I.uUvToScale.value, I.uUvToOffset.value),
              z(y[0], ea, I.uUvCoverScale.value, I.uUvCoverOffset.value),
              r.updateWorldMatrix(!0, !1));
            let eo = w.domElement.getBoundingClientRect(),
              eu = j.thumbnailWidth / 2,
              es = j.thumbnailHeight / 2,
              ec = [
                [-eu + (t ? 0 : -(0.78 * en)), -es + (t ? 0 : -(0.78 * er))],
                [eu + (t ? 0.78 * en : 0), -es + (t ? 0.78 * er : 0)],
                [eu + (t ? 0.78 * en : 0), es + (t ? 0.78 * er : 0)],
                [-eu + (t ? 0 : -(0.78 * en)), es + (t ? 0 : -(0.78 * er))],
              ],
              ed = N.current;
            for (let [e, t] of ((ed.length = 0), ec)) {
              let n = r.localToWorld(new c.Pq0(e, t, 0));
              (n.project(g),
                ed.push(
                  eo.left + (n.x + 1) * eo.width * 0.5,
                  eo.top + (1 - n.y) * eo.height * 0.5,
                ));
            }
            let ep = f.current;
            if (ep && !n)
              if (a <= 0.001)
                ((ep.style.opacity = "0"), (ep.style.clipPath = ""));
              else {
                let e = [],
                  t = Math.PI,
                  n = I.uTravelLag.value.x,
                  i = I.uTravelLag.value.y,
                  l = I.uDepthBend.value,
                  a = I.uMorph.value,
                  u = I.uCoverReturn.value,
                  s = I.uWorldScale.value,
                  d = I.uEdgeMorphStrength.value,
                  p = I.uTime.value,
                  v = Math.max(Math.sin(t * a) * (1 - u), Math.sin(t * u)),
                  h = new c.Pq0(),
                  m = (a, o) => {
                    let u = 2 * a - 1,
                      c = 2 * o - 1,
                      m = Math.pow(Math.abs(u), 1.25),
                      f = Math.pow(Math.abs(c), 1.55),
                      x = m * f,
                      w = Math.sin(a * t),
                      y = Math.sin(o * t);
                    (h.set(
                      (a - 0.5) * j.thumbnailWidth,
                      (o - 0.5) * j.thumbnailHeight,
                      0,
                    ),
                      (h.x += n * (0.125 * x - m * (1 - f) * 0.055)),
                      (h.y += 0.07 * n * u * c),
                      (h.y += 0.025 * i * x),
                      (h.z +=
                        0.48 * l * ((0.95 * w - 0.3 * x) * (0.8 + 0.2 * y))),
                      (h.z +=
                        w *
                        y *
                        v *
                        s *
                        (0.38 + 0.22 * Math.sin(7 * a + 3 * o + 0.4 * p))),
                      (h.x += w * y * v * s * 0.075 * Math.sin(8 * o)));
                    let b = Math.pow(Math.abs(u), 2.6),
                      M = Math.pow(Math.abs(c), 2.6),
                      T =
                        (Math.sin(2 * o * t + 0.5 * p + 0.6) +
                          0.3 * Math.sin(4 * o * t - 0.32 * p)) *
                        y,
                      P =
                        (Math.sin(2 * a * t - 0.4 * p + 1.2) +
                          0.3 * Math.sin(4 * a * t + 0.3 * p)) *
                        w,
                      C = v * s * d;
                    ((h.x += u * b * T * C),
                      (h.y += c * M * P * C * 0.68),
                      (h.z += (b * y + M * w) * C * 0.65),
                      r.localToWorld(h),
                      h.project(g));
                    let k = eo.left + (h.x + 1) * eo.width * 0.5,
                      S = eo.top + (1 - h.y) * eo.height * 0.5;
                    e.push(
                      "".concat(k.toFixed(2), "px ").concat(S.toFixed(2), "px"),
                    );
                  };
                for (let e = 0; e <= 32; e++) m(e / 32, 0);
                for (let e = 1; e <= 32; e++) m(1, e / 32);
                for (let e = 1; e <= 32; e++) m(1 - e / 32, 1);
                for (let e = 1; e <= 32; e++) m(0, 1 - e / 32);
                ((ep.style.clipPath =
                  "polygon(\n          evenodd,\n          0px 0px,\n          "
                    .concat(window.innerWidth, "px 0px,\n          ")
                    .concat(window.innerWidth, "px ")
                    .concat(window.innerHeight, "px,\n          0px ")
                    .concat(
                      window.innerHeight,
                      "px,\n          0px 0px,\n          ",
                    )
                    .concat(e.join(", "), "\n        )")),
                  (ep.style.opacity = String(c.cj9.smoothstep(o, 0, 0.86))));
              }
          }),
          (0, r.jsxs)("group", {
            children: [
              (0, r.jsxs)("mesh", {
                ref: P,
                position: [0, 0, -1],
                renderOrder: 500,
                frustumCulled: !1,
                visible: !1,
                raycast: () => {},
                children: [
                  (0, r.jsx)("planeGeometry", {
                    args: [1.4 * x.width, 1.4 * x.height],
                  }),
                  (0, r.jsx)("meshBasicMaterial", {
                    ref: C,
                    color: "#080808",
                    opacity: 0,
                    transparent: !0,
                    depthTest: !1,
                    depthWrite: !1,
                    toneMapped: !1,
                  }),
                ],
              }),
              (0, r.jsxs)("mesh", {
                ref: T,
                renderOrder: 600,
                frustumCulled: !1,
                raycast: () => {},
                children: [
                  (0, r.jsx)("planeGeometry", {
                    args: [j.thumbnailWidth, j.thumbnailHeight, 64, 88],
                  }),
                  (0, r.jsx)("shaderMaterial", {
                    uniforms: I,
                    vertexShader:
                      "\n  uniform float uTime;\n  uniform float uMorph;\n  uniform float uCoverReturn;\n  uniform float uWorldScale;\n  uniform float uEdgeMorphStrength;\n  uniform float uDepthBend;\n  uniform vec2 uTravelLag;\n  uniform vec2 uImageSize;\n\n  varying vec2 vUv;\n  varying float vProfileShade;\n\n  const float PI = 3.14159265359;\n\n  // X-BEND — KEEP THE SHAPE YOU LIKED\nconst float CORNER_TRAIL = 0.125;  const float SIDE_PULL = 0.055;\n  const float DIAGONAL_TILT = 0.070;\n\n  // DEPTH / LIGHT\n  const float DEPTH_STRENGTH = 0.48;\n  const float LIGHT_STRENGTH = 0.38;\n\n  void main() {\n    vUv = uv;\n\n    vec3 p = position;\n\n    float side = uv.x * 2.0 - 1.0;\n    float verticalSide = uv.y * 2.0 - 1.0;\n\n    float horizontalEdge =\n      pow(abs(side), 1.25);\n\n    float verticalEdge =\n      pow(abs(verticalSide), 1.55);\n\n    float cornerMask =\n      horizontalEdge * verticalEdge;\n\n    float sideMiddle =\n      horizontalEdge * (1.0 - verticalEdge);\n\n    // =====================================\n    // ORIGINAL X-AXIS CORNER TRAILING\n    // =====================================\n\n    p.x += uTravelLag.x * (\n      CORNER_TRAIL * cornerMask -\n      SIDE_PULL * sideMiddle\n    );\n\n    p.y +=\n      uTravelLag.x *\n      DIAGONAL_TILT *\n      side *\n      verticalSide;\n\n    p.y +=\n      uTravelLag.y *\n      0.025 *\n      cornerMask;\n\n    // =====================================\n    // 3D SURFACE CURVATURE\n    // =====================================\n\n    float verticalSoftness =\n      0.80 + 0.20 * sin(uv.y * PI);\n\n    float centerArch =\n      sin(uv.x * PI);\n\n    float depthCurve =\n      (\n        centerArch * 0.95 -\n        cornerMask * 0.30\n      ) *\n      verticalSoftness;\n\n    p.z +=\n      uDepthBend *\n      DEPTH_STRENGTH *\n      depthCurve;\n\n    // =====================================\n    // LIGHT RESPONSE FROM SURFACE SLOPE\n    // =====================================\n\n    // The curve's left and right sides have\n    // different slopes, like a bent sheet.\n    float surfaceSlope =\n      cos(uv.x * PI) *\n      sin(uv.y * PI);\n\n    // Normalize depth against image width,\n    // so lighting remains consistent.\n    float relativeDepth =\n      uDepthBend *\n      DEPTH_STRENGTH /\n      max(uImageSize.x, 1.0);\n\n    float lightDirection =\n      uTravelLag.x >= 0.0 ? 1.0 : -1.0;\n\n    float lighting =\n      surfaceSlope *\n      relativeDepth *\n      LIGHT_STRENGTH *\n      lightDirection;\n\n    // Noticeable, but restrained shading.\n    vProfileShade = clamp(\n      1.0 + lighting,\n      0.86,\n      1.14\n    );\n\n    // =====================================\n    // EXISTING IMAGE / VIDEO MORPH\n    // =====================================\n\n    float sx = sin(uv.x * PI);\n    float sy = sin(uv.y * PI);\n\n    float morphPulse = max(\n      sin(PI * uMorph) *\n        (1.0 - uCoverReturn),\n      sin(PI * uCoverReturn)\n    );\n\n    p.z +=\n      sx * sy *\n      morphPulse *\n      uWorldScale *\n      (\n        0.38 +\n        0.22 * sin(\n          uv.x * 7.0 +\n          uv.y * 3.0 +\n          uTime * 0.4\n        )\n      );\n\n    p.x +=\n      sx * sy *\n      morphPulse *\n      uWorldScale *\n      0.075 *\n      sin(uv.y * 8.0);\n\n    // =====================================\n    // EXISTING MORPH EDGE MOTION\n    // =====================================\n\n    float sideMask =\n      pow(abs(side), 2.6);\n\n    float topBottomMask =\n      pow(abs(verticalSide), 2.6);\n\n    float sideFlow = (\n      sin(\n        uv.y * 6.2831853 +\n        uTime * 0.5 + 0.6\n      ) +\n      0.3 * sin(\n        uv.y * 12.5663706 -\n        uTime * 0.32\n      )\n    ) * sin(uv.y * PI);\n\n    float topBottomFlow = (\n      sin(\n        uv.x * 6.2831853 -\n        uTime * 0.4 + 1.2\n      ) +\n      0.3 * sin(\n        uv.x * 12.5663706 +\n        uTime * 0.3\n      )\n    ) * sin(uv.x * PI);\n\n    float edgeAmount =\n      morphPulse *\n      uWorldScale *\n      uEdgeMorphStrength;\n\n    p.x +=\n      side *\n      sideMask *\n      sideFlow *\n      edgeAmount;\n\n    p.y +=\n      verticalSide *\n      topBottomMask *\n      topBottomFlow *\n      edgeAmount * 0.68;\n\n    p.z += (\n      sideMask * sin(uv.y * PI) +\n      topBottomMask * sin(uv.x * PI)\n    ) * edgeAmount * 0.65;\n\n    gl_Position =\n      projectionMatrix *\n      modelViewMatrix *\n      vec4(p, 1.0);\n  }\n",
                    fragmentShader: R,
                    transparent: !0,
                    depthTest: !1,
                    depthWrite: !1,
                    toneMapped: !1,
                    side: c.$EB,
                  }),
                ],
              }),
            ],
          })
        );
      }
      let D = [
          {
            label: "Profile",
            title: "RUSTAM KERIMOV",
            intro:
              "A graphic designer exploring visual identities, typography and motion.",
            description:
              "Creating distinctive visual experiences across branding, editorial design, art direction and animation.",
            mobile:
              "A graphic designer exploring visual identities, typography, art direction and motion.",
          },
          {
            label: "Visual Identities",
            title: "VISUAL IDENTITIES",
            intro:
              "Building distinctive visual systems that give brands a clear and recognizable voice.",
            description:
              "From typography and color to composition and visual direction, every element works together to create a cohesive identity.",
            mobile:
              "Creating distinctive visual identities through typography, color and considered design systems.",
          },
          {
            label: "Logo Design",
            title: "LOGO DESIGN",
            intro:
              "Creating memorable marks that turn ideas into recognizable visual signatures.",
            description:
              "Exploring shape, proportion and typography to develop logos that feel purposeful, distinctive and versatile.",
            mobile:
              "Creating distinctive and memorable logos through shape, typography and visual exploration.",
          },
          {
            label: "Art Direction",
            title: "ART DIRECTION",
            intro:
              "Shaping visual experiences through a clear creative perspective.",
            description:
              "Connecting imagery, typography and composition to establish a distinctive direction and bring creative ideas together.",
            mobile:
              "Shaping creative ideas through imagery, typography and a considered visual direction.",
          },
          {
            label: "Motion & Animation",
            title: "MOTION & ANIMATION",
            intro:
              "Bringing graphic design to life through movement, rhythm and timing.",
            description:
              "Exploring how motion can add character, energy and an entirely new dimension to visual communication.",
            mobile:
              "Bringing design to life through movement, rhythm, animation and visual storytelling.",
          },
          {
            label: "Editorial Design",
            title: "EDITORIAL DESIGN",
            intro:
              "Exploring the relationship between typography, imagery and space.",
            description:
              "Creating expressive editorial layouts that balance visual structure, storytelling and experimental design.",
            mobile:
              "Creating expressive editorial experiences through typography, imagery and considered composition.",
          },
        ],
        H = [0.16, 1, 0.3, 1],
        F = {
          hidden: {},
          visible: { transition: { delayChildren: 0, staggerChildren: 0.035 } },
          exit: { opacity: 0, transition: { duration: 0.25, ease: "easeOut" } },
        },
        W = { hidden: {}, visible: { transition: { staggerChildren: 0.025 } } },
        Y = {
          hidden: { y: "115%", opacity: 0, filter: "blur(3px)" },
          visible: {
            y: "0%",
            opacity: 1,
            filter: "blur(0px)",
            transition: { duration: 0.7, ease: H },
          },
        },
        X = {
          hidden: { opacity: 0 },
          visible: { opacity: 1, transition: { duration: 0.2 } },
        },
        G = {
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: { opacity: { duration: 0.75, ease: H } },
          },
          exit: {
            opacity: 0,
            transition: { duration: 0.45, ease: "easeInOut" },
          },
        },
        _ = {
          hidden: { opacity: 0 },
          visible: { opacity: 1, transition: { duration: 0.2 } },
          exit: { opacity: 0, transition: { duration: 0.15 } },
        };
      function q(e) {
        var t;
        let {
            text: n,
            delay: i = 0,
            stagger: l = 0.015,
            reducedMotion: a = !1,
            inline: o = !1,
          } = e,
          u = null != (t = n.match(/\S+|\s+/g)) ? t : [];
        return (0, r.jsx)(y.P.span, {
          className: o
            ? "inline-block whitespace-pre-line"
            : "block whitespace-pre-line",
          variants: {
            hidden: {},
            visible: {
              transition: {
                delayChildren: a ? 0 : i,
                staggerChildren: a ? 0 : l,
              },
            },
          },
          children: u.map((e, t) =>
            /^\s+$/.test(e)
              ? (0, r.jsx)("span", { children: e }, t)
              : (0, r.jsx)(
                  "span",
                  {
                    className:
                      "inline-block overflow-hidden align-bottom pb-[0.12em] -mb-[0.12em]",
                    children: (0, r.jsx)(y.P.span, {
                      className: "inline-block will-change-transform",
                      variants: a ? X : Y,
                      children: e,
                    }),
                  },
                  t,
                ),
          ),
        });
      }
      function V(e) {
        var t, n;
        let {
            visible: i,
            mediaIndex: l,
            onSelectMedia: a,
            onMenuHoverChange: o,
          } = e,
          u = null != (t = (0, b.I)()) && t,
          s = null != (n = D[l]) ? n : D[0],
          c =
            s.title.length > 15
              ? "text-[clamp(15px,1.35vw,24px)]"
              : "text-[clamp(20px,1.7vw,32px)]",
          d = u ? _ : G;
        return (0, r.jsx)(M.N, {
          children:
            i &&
            (0, r.jsxs)(
              y.P.div,
              {
                initial: "hidden",
                animate: "visible",
                exit: "exit",
                variants: F,
                className:
                  "pointer-events-none absolute inset-0 z-[50] text-[#e7e3dd]",
                children: [
                  (0, r.jsx)(y.P.div, {
                    variants: W,
                    className:
                      "absolute left-[5%] top-[10%] w-[90%] lg:left-[3.5%] lg:top-[27%] lg:w-[21%]",
                    children: (0, r.jsx)("div", {
                      className: "grid grid-cols-1",
                      children: (0, r.jsxs)(M.N, {
                        mode: "sync",
                        children: [
                          " ",
                          (0, r.jsxs)(
                            y.P.div,
                            {
                              variants: d,
                              initial: "hidden",
                              animate: "visible",
                              exit: "exit",
                              className: "col-start-1 row-start-1 min-w-0",
                              children: [
                                (0, r.jsx)("h2", {
                                  className:
                                    "font-bueno whitespace-nowrap font-bold uppercase leading-[1.05] tracking-[-0.025em] ".concat(
                                      c,
                                    ),
                                  children: (0, r.jsx)(q, {
                                    text: s.title,
                                    stagger: 0.025,
                                    reducedMotion: u,
                                  }),
                                }),
                                (0, r.jsxs)(y.P.div, {
                                  variants: W,
                                  className:
                                    "mt-5 hidden font-bueno text-[clamp(15px,1.08vw,19px)] leading-[1.55] text-[#e7e3dd]/80 lg:block",
                                  children: [
                                    (0, r.jsx)("p", {
                                      children: (0, r.jsx)(q, {
                                        text: s.intro,
                                        stagger: 0.016,
                                        reducedMotion: u,
                                      }),
                                    }),
                                    (0, r.jsx)("p", {
                                      className: "mt-6",
                                      children: (0, r.jsx)(q, {
                                        text: s.description,
                                        stagger: 0.016,
                                        reducedMotion: u,
                                      }),
                                    }),
                                  ],
                                }),
                              ],
                            },
                            "about-content-".concat(l),
                          ),
                        ],
                      }),
                    }),
                  }),
                  (0, r.jsx)(y.P.div, {
                    variants: W,
                    onPointerEnter: () => (null == o ? void 0 : o(!0)),
                    onPointerLeave: () => (null == o ? void 0 : o(!1)),
                    onPointerDown: (e) => e.stopPropagation(),
                    onPointerUp: (e) => e.stopPropagation(),
                    className:
                      "pointer-events-auto absolute bottom-[5%] right-[3.1%] hidden w-[22%] text-right lg:block",
                    children: (0, r.jsx)("div", {
                      className:
                        "flex flex-col items-end font-bueno text-[clamp(16px,1.1vw,19px)] font-medium leading-[1.4]",
                      children: D.map((e, t) =>
                        (0, r.jsx)(
                          "button",
                          {
                            type: "button",
                            "aria-current": l === t ? "true" : void 0,
                            onClick: (e) => {
                              (e.stopPropagation(), a(t));
                            },
                            className:
                              "cursor-pointer whitespace-nowrap text-right transition-opacity duration-500 ease-in-out hover:!opacity-100 focus-visible:!opacity-100 focus-visible:outline focus-visible:outline-1 focus-visible:outline-offset-2 focus-visible:outline-[#e7e3dd]",
                            style: { opacity: l === t ? 1 : 0.3 },
                            children: (0, r.jsx)(q, {
                              text: e.label,
                              delay: 0.02 + 0.018 * t,
                              stagger: 0.012,
                              reducedMotion: u,
                            }),
                          },
                          e.label,
                        ),
                      ),
                    }),
                  }),
                  (0, r.jsx)(y.P.div, {
                    variants: W,
                    className:
                      "absolute bottom-[12%] left-[5%] right-[5%] lg:hidden",
                    children: (0, r.jsx)("div", {
                      className: "grid grid-cols-1",
                      children: (0, r.jsx)(M.N, {
                        mode: "sync",
                        initial: !1,
                        children: (0, r.jsxs)(
                          y.P.div,
                          {
                            variants: d,
                            initial: "hidden",
                            animate: "visible",
                            exit: "exit",
                            className: "col-start-1 row-start-1 min-w-0",
                            children: [
                              (0, r.jsx)("p", {
                                className:
                                  "mb-2 font-bueno text-[13px] leading-[1.4] text-[#e7e3dd]/80",
                                children: (0, r.jsx)(q, {
                                  text: s.mobile,
                                  stagger: 0.015,
                                  reducedMotion: u,
                                }),
                              }),
                              (0, r.jsx)("p", {
                                className:
                                  "font-bueno text-[12px] uppercase tracking-[0.08em] text-[#e7e3dd]/65",
                                children: (0, r.jsx)(q, {
                                  text: s.label,
                                  reducedMotion: u,
                                }),
                              }),
                            ],
                          },
                          "mobile-about-".concat(l),
                        ),
                      }),
                    }),
                  }),
                  (0, r.jsxs)(y.P.div, {
                    variants: W,
                    className:
                      "absolute bottom-[4%] left-[5%] right-[5%] grid grid-cols-2 items-end gap-2 lg:bottom-[5%] lg:left-[5.3%] lg:right-auto lg:flex lg:items-end lg:gap-7",
                    children: [
                      (0, r.jsx)("div", {
                        className: "min-w-0",
                        children: (0, r.jsx)("p", {
                          className:
                            "font-sans text-[9px] font-medium uppercase leading-[1.4] tracking-[0.16em] text-[#e7e3dd]/80 md:text-[10px]",
                          children: (0, r.jsx)(q, {
                            text: "Scroll or click to explore",
                            stagger: 0.016,
                            reducedMotion: u,
                          }),
                        }),
                      }),
                      (0, r.jsxs)("div", {
                        className:
                          "flex min-w-0 flex-col items-end gap-1 text-right font-sans text-[9px] font-medium uppercase leading-[1.4] tracking-[0.16em] text-[#e7e3dd]/80 md:flex-row md:justify-end md:gap-3 md:text-[10px] lg:justify-start",
                        children: [
                          (0, r.jsx)("span", {
                            className: "whitespace-nowrap",
                            children: (0, r.jsx)(q, {
                              text: "Oslo, Norway",
                              inline: !0,
                              reducedMotion: u,
                            }),
                          }),
                          (0, r.jsx)("span", {
                            className: "hidden opacity-40 md:inline",
                            children: "/",
                          }),
                          (0, r.jsx)("span", {
                            className: "whitespace-nowrap",
                            children: (0, r.jsx)(q, {
                              text: "Age: 27",
                              inline: !0,
                              reducedMotion: u,
                            }),
                          }),
                        ],
                      }),
                    ],
                  }),
                ],
              },
              "rustam-profile-info",
            ),
        });
      }
      var $ = n(4760);
      let K = (e) => c.cj9.clamp(e, 0, 1),
        J = (e) => 1 + 2 * Math.pow(e - 1, 3) + +Math.pow(e - 1, 2);
      function Q(e) {
        if (!(e instanceof c.eaF)) return !1;
        let t = e.material;
        return (
          t instanceof c.BKk &&
          !!(t.uniforms.uOpacity && t.uniforms.uPointer && t.uniforms.uHover)
        );
      }
      function Z(e) {
        let { start: t } = e,
          { scene: n, size: r } = (0, u.A)(),
          i = (0, o.useRef)(null),
          l = (0, o.useRef)(!1),
          a = (0, o.useRef)([]);
        return (
          (0, u.C)((e) => {
            let { clock: o } = e;
            if (l.current) return;
            if (!t)
              return void n.traverse((e) => {
                Q(e) && (e.material.uniforms.uOpacity.value = 0);
              });
            if (null === i.current) {
              i.current = o.elapsedTime;
              let e = [],
                t = r.width / 2;
              (n.traverse((n) => {
                if (!Q(n)) return;
                let r = n.material;
                if (300 === n.renderOrder) {
                  r.uniforms.uOpacity.value = 1;
                  return;
                }
                n.visible && n.position.x > -t - 200 && n.position.x < t + 200
                  ? ((r.uniforms.uOpacity.value = 0), e.push(n))
                  : (r.uniforms.uOpacity.value = 1);
              }),
                e.sort((e, t) => e.position.x - t.position.x),
                (a.current = (function (e) {
                  let t = [],
                    n = 0,
                    r = e.length - 1;
                  for (; n <= r;)
                    (n === r ? t.push(e[n]) : (t.push(e[n]), t.push(e[r])),
                      n++,
                      r--);
                  return t;
                })(e).map((e, t) => ({ mesh: e, delay: 0.075 * t }))));
            }
            let u = o.elapsedTime - i.current,
              s = !0;
            for (let { mesh: e, delay: t } of a.current) {
              let n = e.material;
              if (300 === e.renderOrder) {
                n.uniforms.uOpacity.value = 1;
                continue;
              }
              let i = K((u - t) / 1.15),
                l = J(i);
              ((n.uniforms.uOpacity.value = c.cj9.smoothstep(i, 0, 0.55)),
                (e.position.y -= 0.38 * r.height * (1 - l)),
                i < 1 && (s = !1));
            }
            s &&
              ((l.current = !0),
              n.traverse((e) => {
                Q(e) && (e.material.uniforms.uOpacity.value = 1);
              }));
          }),
          null
        );
      }
      let ee = [0.16, 1, 0.3, 1],
        et = {
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: { duration: 0.4, staggerChildren: 0.08 },
          },
          exit: { opacity: 0, transition: { duration: 0.35, ease: ee } },
        },
        en = {
          hidden: { y: "115%", opacity: 0, filter: "blur(3px)" },
          visible: {
            y: "0%",
            opacity: 1,
            filter: "blur(0px)",
            transition: { duration: 0.85, ease: ee },
          },
        };
      function er(e) {
        let { text: t, stagger: n = 0.045, reducedMotion: i } = e;
        return (0, r.jsx)(y.P.span, {
          className: "block",
          variants: {
            hidden: {},
            visible: { transition: { staggerChildren: i ? 0 : n } },
          },
          children: t
            .split(" ")
            .map((e, t) =>
              (0, r.jsx)(
                "span",
                {
                  className:
                    "mr-[0.24em] inline-block overflow-hidden align-bottom pb-[0.1em] -mb-[0.1em]",
                  children: (0, r.jsx)(y.P.span, {
                    className: "inline-block will-change-transform",
                    variants: i
                      ? { hidden: { opacity: 0 }, visible: { opacity: 1 } }
                      : en,
                    children: e,
                  }),
                },
                "".concat(e, "-").concat(t),
              ),
            ),
        });
      }
      function ei(e) {
        var t;
        let { visible: n } = e,
          i = null != (t = (0, b.I)()) && t;
        return (0, r.jsx)(M.N, {
          children:
            n &&
            (0, r.jsxs)(
              y.P.div,
              {
                initial: "hidden",
                animate: "visible",
                exit: "exit",
                variants: et,
                className:
                  "pointer-events-none absolute inset-0 z-[20] text-color",
                children: [
                  (0, r.jsx)(y.P.div, {
                    className:
                      " absolute left-[5%] top-[105px] w-[90%] lg:left-[3.1%] lg:top-[32%] lg:w-[70%] ",
                    variants: {
                      hidden: {},
                      visible: { transition: { staggerChildren: 0.12 } },
                    },
                    children: (0, r.jsxs)("h1", {
                      className:
                        " text-[clamp(22px,4.2vw,32px)] font-bold leading-[1.1] tracking-[-0.035em] lg:text-[clamp(25px,2.15vw,38px)] ",
                      children: [
                        (0, r.jsx)("div", {
                          className: "lg:whitespace-nowrap",
                          children: (0, r.jsx)(er, {
                            text: "GRAPHIC DESIGNER",
                            stagger: 0.06,
                            reducedMotion: i,
                          }),
                        }),
                        (0, r.jsx)("div", {
                          className: "lg:whitespace-nowrap",
                          children: (0, r.jsx)(er, {
                            text: "CRAFTING VISUAL IDENTITIES,",
                            stagger: 0.045,
                            reducedMotion: i,
                          }),
                        }),
                        (0, r.jsx)("div", {
                          className: "lg:whitespace-nowrap",
                          children: (0, r.jsx)(er, {
                            text: "TYPOGRAPHY AND MOTION.",
                            stagger: 0.045,
                            reducedMotion: i,
                          }),
                        }),
                      ],
                    }),
                  }),
                  (0, r.jsx)(y.P.div, {
                    className:
                      " absolute right-[5%] top-[225px] w-[clamp(104px,28vw,140px)] lg:bottom-0 lg:right-[3.1%] lg:top-0 lg:w-[clamp(150px,12vw,210px)] ",
                    variants: {
                      hidden: {},
                      visible: { transition: { delayChildren: 0.4 * !i } },
                    },
                    children: (0, r.jsx)("div", {
                      className:
                        " aspect-[4/5] lg:absolute lg:left-0 lg:top-[150px] lg:w-full ",
                    }),
                  }),
                ],
              },
              "hero-intro",
            ),
        });
      }
      let el = [0.16, 1, 0.3, 1],
        ea = {
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: { duration: 0.4, delayChildren: 0.48 },
          },
          exit: { opacity: 0, transition: { duration: 0.35, ease: el } },
        },
        eo = {
          hidden: { y: "115%", opacity: 0, filter: "blur(3px)" },
          visible: {
            y: "0%",
            opacity: 1,
            filter: "blur(0px)",
            transition: { duration: 0.85, ease: el },
          },
        };
      function eu(e) {
        let { text: t, stagger: n = 0.018, reducedMotion: i } = e;
        return (0, r.jsx)(y.P.span, {
          className: "block",
          variants: {
            hidden: {},
            visible: { transition: { staggerChildren: i ? 0 : n } },
          },
          children: t
            .split(" ")
            .map((e, t) =>
              (0, r.jsx)(
                "span",
                {
                  className:
                    "mr-[0.24em] inline-block overflow-hidden align-bottom pb-[0.1em] -mb-[0.1em]",
                  children: (0, r.jsx)(y.P.span, {
                    className: "inline-block will-change-transform",
                    variants: i
                      ? { hidden: { opacity: 0 }, visible: { opacity: 1 } }
                      : eo,
                    children: e,
                  }),
                },
                "".concat(e, "-").concat(t),
              ),
            ),
        });
      }
      function es(e) {
        var t;
        let { visible: n } = e,
          i = null != (t = (0, b.I)()) && t;
        return (0, r.jsx)(M.N, {
          children:
            n &&
            (0, r.jsx)(
              y.P.div,
              {
                initial: "hidden",
                animate: "visible",
                exit: "exit",
                variants: ea,
                className:
                  " pointer-events-none absolute inset-0 z-[20] text-color ",
                children: (0, r.jsxs)("div", {
                  className:
                    " absolute right-[5%] top-[225px] w-[clamp(104px,28vw,140px)]  lg:top-auto lg:bottom-[calc(21svh+32px)] lg:right-[3.1%] lg:w-[clamp(150px,12vw,210px)]  [@media(min-width:1024px)_and_(max-height:680px)]:hidden ",
                  children: [
                    (0, r.jsx)("div", { className: "aspect-[4/5] lg:hidden" }),
                    (0, r.jsx)("div", {
                      className:
                        " mt-7 w-[min(62vw,290px)] -translate-x-[50%]  lg:absolute lg:bottom-0 lg:left-0 lg:mt-0 lg:w-[clamp(360px,29vw,500px)] lg:-translate-x-[55%] ",
                      children: (0, r.jsx)("p", {
                        className:
                          " text-[14px] leading-[1.45] tracking-[-0.025em] text-color lg:text-[17px] ",
                        children: (0, r.jsx)(eu, {
                          text: "Take a look at my selected projects below to see what I've been working on. I'm always open to new projects, fresh ideas and creative collaborations, so feel free to get in touch.",
                          stagger: 0.018,
                          reducedMotion: i,
                        }),
                      }),
                    }),
                  ],
                }),
              },
              "project-intro",
            ),
        });
      }
      let ec = (e) => e.replace(/\/+$/, "") || "/";
      function ed(e) {
        let t = e.match(/^\/project\/([^/]+)\/?$/);
        if (!t) return null;
        try {
          return decodeURIComponent(t[1]);
        } catch (e) {
          return null;
        }
      }
      function ep(e) {
        var t, n, u, s, d, p, v, h;
        let { projects: m } = e,
          y = (0, l.usePathname)(),
          [b, M] = (0, o.useState)(() => ec(y));
        ((0, o.useEffect)(() => {
          M(ec(y));
        }, [y]),
          (0, o.useEffect)(() => {
            let e = () => {
              M(ec(window.location.pathname));
            };
            return (
              window.addEventListener("popstate", e),
              () => {
                window.removeEventListener("popstate", e);
              }
            );
          }, []));
        let [j, T] = (0, o.useState)(!1),
          [P, C] = (0, o.useState)(!1),
          [k, S] = (0, o.useState)(!1),
          [R, A] = (0, o.useState)(!1),
          [O, U] = (0, o.useState)(!1),
          [L, z] = (0, o.useState)(0),
          [D, H] = (0, o.useState)(!1),
          [F, W] = (0, o.useState)(!1),
          [Y, X] = (0, o.useState)(0),
          G = (0, o.useRef)(null),
          _ = (0, o.useRef)(null),
          [q, K] = (0, o.useState)(!1),
          [J, Q] = (0, o.useState)(!1),
          ee = (0, o.useCallback)(() => {
            Q(!0);
          }, []),
          et = (0, o.useCallback)(() => {
            K(!0);
          }, []),
          en = (0, o.useRef)(y),
          er = (0, o.useRef)(
            m.findIndex((e) => String(e.id) === ed(en.current)),
          ),
          el = (0, o.useRef)(null),
          ea = (0, o.useRef)({ value: 0 }),
          eo = (0, o.useRef)(null),
          eu = (0, o.useRef)({ value: 0 }),
          ep = (0, o.useRef)(null),
          ev = (0, o.useRef)(null),
          eh = (0, o.useRef)(0),
          em = (0, o.useRef)(null),
          ef = (0, o.useRef)(null),
          ex = (0, o.useRef)(null),
          eg = (0, o.useRef)(null),
          ew = (0, o.useCallback)((e) => {
            let t = ec(e);
            (ec(window.location.pathname) !== t &&
              window.history.pushState(null, "", t),
              M(t));
          }, []),
          ey = (0, o.useCallback)(
            (e) => {
              let t = m[e.index];
              t &&
                ((el.current = e),
                ew("/project/".concat(encodeURIComponent(String(t.id)))));
            },
            [m, ew],
          ),
          {
            containerRef: eb,
            backdropRef: eM,
            scrollTarget: ej,
            titleRef: eT,
            pressedRef: eP,
            pressedPlaneRef: eC,
            selected: ek,
            progress: eS,
            handleHoverChange: eN,
            openProject: eI,
            closeProject: eR,
            closingRef: eE,
            imageProgress: eA,
            coverMorph: eO,
            hovered: eU,
            closing: eL,
            detailsReady: ez,
            currentMediaIndex: eB,
            onPointerDown: eD,
            onPointerMove: eH,
            onPointerUp: eF,
            onPointerCancel: eW,
          } = (function (e, t, n, r) {
            let i = (0, o.useRef)(null),
              l = (0, o.useRef)(null),
              u = (0, o.useRef)(0),
              s = (0, o.useRef)(null),
              d = (0, o.useRef)(null),
              p = (0, o.useRef)(null),
              v = (0, o.useRef)(!1),
              h = (0, o.useRef)(null),
              m = (0, o.useRef)(null),
              f = (0, o.useRef)(null),
              x = (0, o.useRef)({ value: 0 }),
              g = (0, o.useRef)({ value: 0 }),
              w = (0, o.useRef)({ value: 0 }),
              y = (0, o.useRef)(null),
              b = (0, o.useRef)(null),
              M = (0, o.useRef)(0),
              j = (0, o.useRef)(!1),
              T = (0, o.useRef)({ active: !1, startX: 0, lastX: 0, moved: !1 }),
              [P, C] = (0, o.useState)(null),
              [k, S] = (0, o.useState)(null),
              [N, I] = (0, o.useState)(!1),
              [R, E] = (0, o.useState)(!1),
              [A, O] = (0, o.useState)(0),
              U = (0, o.useRef)(0),
              L = (0, o.useCallback)((e) => {
                h.current || C(e);
              }, []),
              z = (0, o.useCallback)((e) => {
                let t = h.current;
                if (t) {
                  t.index === e.index && t.copy === e.copy && (v.current = !0);
                  return;
                }
                ((d.current = e), (p.current = e));
              }, []),
              B = (0, o.useCallback)(
                function (e) {
                  var t, r, i;
                  let l =
                    !(arguments.length > 1) ||
                    void 0 === arguments[1] ||
                    arguments[1];
                  h.current ||
                    (null == (t = m.current) || t.kill(),
                    null == (r = b.current) || r.kill(),
                    null == (i = y.current) || i.kill(),
                    (w.current.value = 0),
                    (g.current.value = 0),
                    (M.current = 0),
                    (v.current = !1),
                    (U.current = 0),
                    O(0),
                    null !== f.current && window.clearTimeout(f.current),
                    (h.current = e),
                    (j.current = !1),
                    (x.current.value = 0),
                    S(e),
                    C(null),
                    I(!1),
                    E(!1),
                    l && (null == n || n(e)),
                    (f.current = window.setTimeout(() => {
                      ((f.current = null),
                        j.current ||
                          h.current !== e ||
                          (m.current = a.Ay.to(x.current, {
                            value: 1,
                            duration: 0.9,
                            ease: "none",
                            overwrite: !0,
                            onComplete: () => {
                              j.current || h.current !== e || E(!0);
                            },
                          })));
                    }, 100)));
                },
                [n],
              ),
              D = (0, o.useCallback)(
                function () {
                  var e, t, n;
                  let i =
                    !(arguments.length > 0) ||
                    void 0 === arguments[0] ||
                    arguments[0];
                  if (!h.current || j.current) return;
                  (i && (null == r || r()),
                    (j.current = !0),
                    I(!0),
                    E(!1),
                    null !== f.current &&
                      (window.clearTimeout(f.current), (f.current = null)),
                    null == (e = m.current) || e.kill(),
                    null == (t = b.current) || t.kill(),
                    null == (n = y.current) || n.kill(),
                    (M.current = 0),
                    (v.current = !1));
                  let l = () => {
                    m.current = a.Ay.to(x.current, {
                      value: 0,
                      duration: Math.max(0.2, 0.9 * x.current.value),
                      ease: "none",
                      overwrite: !0,
                      onComplete: () => {
                        ((h.current = null),
                          (j.current = !1),
                          (x.current.value = 0),
                          (g.current.value = 0),
                          (w.current.value = 0),
                          (U.current = 0),
                          O(0),
                          S(null),
                          I(!1));
                      },
                    });
                  };
                  g.current.value > 0.01
                    ? ((w.current.value = 0),
                      (y.current = a.Ay.to(w.current, {
                        value: 1,
                        duration: 1.08,
                        ease: "power3.inOut",
                        overwrite: !0,
                        onComplete: l,
                      })))
                    : l();
                },
                [r],
              ),
              H = (0, o.useCallback)(
                function (t) {
                  var n, r, i;
                  let l =
                      arguments.length > 1 &&
                      void 0 !== arguments[1] &&
                      arguments[1],
                    o = h.current;
                  if (!o || j.current || x.current.value < 0.98) return;
                  let u = e[o.index];
                  if (!u) return;
                  let s =
                    1 +
                    (null != (i = u.images) ? i : []).filter(
                      (e) => e && e !== u.src,
                    ).length +
                    +(null != (n = u.srcVideo) && !!n.trim());
                  if (
                    s < 2 ||
                    (null == (r = b.current) ? void 0 : r.isActive())
                  )
                    return;
                  let d = Math.round(g.current.value),
                    p = l && t > 0 && d === s - 1,
                    v = p ? s : c.cj9.clamp(d + t, 0, s - 1);
                  v !== d &&
                    (b.current = a.Ay.to(g.current, {
                      value: v,
                      duration: 1.08,
                      ease: "power3.inOut",
                      overwrite: !0,
                      onUpdate: () => {
                        let e = p
                          ? Math.round(g.current.value) % s
                          : c.cj9.clamp(Math.round(g.current.value), 0, s - 1);
                        e !== U.current && ((U.current = e), O(e));
                      },
                      onComplete: () => {
                        p && (g.current.value = 0);
                        let e = p ? 0 : v;
                        ((U.current = e), O(e));
                      },
                    }));
                },
                [e],
              );
            return (
              (0, o.useEffect)(() => {
                let e = i.current;
                if (!e) return;
                let t = (t) => {
                  (t.preventDefault(), t.stopPropagation());
                  let n = h.current,
                    r =
                      1 === t.deltaMode
                        ? 16
                        : 2 === t.deltaMode
                          ? e.clientHeight
                          : 1,
                    i =
                      Math.abs(t.deltaX) > Math.abs(t.deltaY)
                        ? t.deltaX
                        : t.deltaY;
                  if (n) {
                    if (
                      j.current ||
                      x.current.value < 0.98 ||
                      ((M.current += i * r), 65 > Math.abs(M.current))
                    )
                      return;
                    let e = Math.sign(M.current);
                    ((M.current = 0), H(e, !0));
                    return;
                  }
                  u.current += i * r;
                };
                return (
                  e.addEventListener("wheel", t, { passive: !1 }),
                  () => e.removeEventListener("wheel", t)
                );
              }, [H]),
              (0, o.useEffect)(() => {
                let e = (e) => {
                  "Escape" === e.key && D();
                };
                return (
                  window.addEventListener("keydown", e),
                  () => window.removeEventListener("keydown", e)
                );
              }, [D]),
              (0, o.useEffect)(
                () => () => {
                  var e, t, n;
                  (null == (e = m.current) || e.kill(),
                    null == (t = b.current) || t.kill(),
                    null == (n = y.current) || n.kill(),
                    null !== f.current && window.clearTimeout(f.current));
                },
                [],
              ),
              {
                containerRef: i,
                backdropRef: l,
                scrollTarget: u,
                titleRef: s,
                pressedRef: d,
                pressedPlaneRef: p,
                selected: k,
                progress: x,
                handleHoverChange: L,
                handlePress: z,
                openProject: B,
                closingRef: j,
                imageProgress: g,
                coverMorph: w,
                hovered: P,
                closing: N,
                detailsReady: R,
                currentMediaIndex: A,
                closeProject: D,
                onPointerDown: (e) => {
                  ("mouse" !== e.pointerType || 0 === e.button) &&
                    (e.target.closest("button") ||
                      ((T.current = {
                        active: !0,
                        startX: e.clientX,
                        lastX: e.clientX,
                        moved: !1,
                      }),
                      e.currentTarget.setPointerCapture(e.pointerId)));
                },
                onPointerMove: (e) => {
                  let t = T.current;
                  t.active &&
                    (Math.abs(e.clientX - t.startX) > 6 && (t.moved = !0),
                    t.moved &&
                      !h.current &&
                      ((p.current = null), (u.current -= e.clientX - t.lastX)),
                    (t.lastX = e.clientX));
                },
                onPointerUp: (n) => {
                  if (T.current.active) {
                    if (
                      ((T.current.moved || !d.current) && (p.current = null),
                      !T.current.moved)
                    )
                      if (h.current)
                        if (
                          t.current
                            ? t.current(n.clientX, n.clientY)
                            : v.current
                        ) {
                          var r, i;
                          let t = h.current,
                            n = t ? e[t.index] : null;
                          (n
                            ? 1 +
                              (null != (i = n.images) ? i : []).filter(
                                (e) => e && e !== n.src,
                              ).length +
                              +(null != (r = n.srcVideo) && !!r.trim())
                            : 0) < 2
                            ? D()
                            : H(1, !0);
                        } else D();
                      else d.current && B(d.current);
                    ((T.current.active = !1),
                      (d.current = null),
                      (v.current = !1));
                  }
                },
                onPointerCancel: () => {
                  ((T.current.active = !1),
                    (d.current = null),
                    (p.current = null),
                    (v.current = !1));
                },
              }
            );
          })(
            m,
            ef,
            ey,
            (0, o.useCallback)(() => {
              ew("/");
            }, [ew]),
          ),
          eY = (0, o.useCallback)(
            (e) => {
              (eN(e), T(!!e));
            },
            [eN],
          ),
          eX = (0, o.useCallback)(() => {
            (C(!1),
              U(!1),
              A(!1),
              z(0),
              H(!1),
              (eo.current = null),
              (ea.current.value = 0),
              (eu.current.value = 0),
              (eh.current = 0));
          }, []),
          eG = (0, o.useCallback)(
            function () {
              var e, t;
              let n =
                !(arguments.length > 0) ||
                void 0 === arguments[0] ||
                arguments[0];
              P ||
                ek ||
                eL ||
                (null == (e = ep.current) || e.kill(),
                null == (t = ev.current) || t.kill(),
                (eo.current = null),
                (ea.current.value = 0),
                (eu.current.value = 0),
                (eh.current = 0),
                z(0),
                A(!1),
                U(!1),
                C(!0),
                S(!0),
                T(!1),
                eN(null),
                n && ew("/about"));
            },
            [P, ek, eL, eN, ew],
          ),
          e_ = (0, o.useCallback)(
            function () {
              var e, t;
              let n =
                !(arguments.length > 0) ||
                void 0 === arguments[0] ||
                arguments[0];
              if (P && !R) {
                if (
                  (A(!0),
                  U(!1),
                  null == (e = ep.current) || e.kill(),
                  eo.current)
                ) {
                  let e = eo.current;
                  ((ea.current.value = e.progress >= 0.5 ? e.to : e.from),
                    (eo.current = null));
                }
                (H(!1),
                  (eh.current = 0),
                  n && ew("/"),
                  ea.current.value > 0.001
                    ? (null == (t = ev.current) || t.kill(),
                      (ev.current = a.Ay.to(eu.current, {
                        value: 1,
                        duration: 1.08,
                        ease: "power3.inOut",
                        overwrite: !0,
                        onComplete: () => {
                          S(!1);
                        },
                      })))
                    : S(!1));
              }
            },
            [P, R, ew],
          ),
          eq = (0, o.useCallback)(() => {
            (ew("/about"), ek || eL || P || R || eG(!1));
          }, [ew, ek, eL, P, R, eG]);
        ((0, o.useEffect)(
          () => (
            window.addEventListener("rustam:open-profile", eq),
            () => {
              window.removeEventListener("rustam:open-profile", eq);
            }
          ),
          [eq],
        ),
          (0, o.useEffect)(() => {
            let e = ed(b);
            if ("/about" === b) {
              if (ek) {
                eL || eR(!1);
                return;
              }
              if (R) return;
              P || eG(!1);
              return;
            }
            if (P) {
              R || e_(!1);
              return;
            }
            if (null !== e) {
              if (!q) return;
              let t = m.findIndex((t) => String(t.id) === e);
              if (t < 0) return;
              if (ek) {
                ek.index === t || eL || eR(!1);
                return;
              }
              if (eL) return;
              let n = el.current;
              eI(
                (null == n ? void 0 : n.index) === t
                  ? n
                  : { index: t, copy: 0 },
                !1,
              );
              return;
            }
            ek && !eL && eR(!1);
          }, [b, m, ek, eL, P, q, R, eI, eR, eG, e_]));
        let eV = (0, o.useCallback)(
            (e) => {
              var t;
              if (
                !k ||
                !O ||
                R ||
                (null == (t = ep.current) ? void 0 : t.isActive())
              )
                return;
              let n = E.length,
                r = Math.round(ea.current.value) % n,
                i = e > 0 ? (r === n - 1 ? n : r + 1) : Math.max(0, r - 1);
              i !== r &&
                (ep.current = a.Ay.to(ea.current, {
                  value: i,
                  duration: 1.08,
                  ease: "power3.inOut",
                  overwrite: !0,
                  onUpdate: () => {
                    let t = ea.current.value,
                      l =
                        e > 0
                          ? t - r >= 0.5
                            ? (r + 1) % n
                            : r
                          : t - i >= 0.5
                            ? r
                            : i;
                    z((e) => (e === l ? e : l));
                  },
                  onComplete: () => {
                    let e = i === n ? 0 : i;
                    (i === n && (ea.current.value = 0), z(e));
                  },
                }));
            },
            [k, O, R],
          ),
          e$ = (0, o.useCallback)(
            (e) => {
              var t;
              if (
                !k ||
                !O ||
                R ||
                (null == (t = ep.current) ? void 0 : t.isActive()) ||
                e < 0 ||
                e >= E.length
              )
                return;
              let n = E.length,
                r = Math.round(ea.current.value) % n;
              if (r === e) return;
              if (e === r + 1 || (r === n - 1 && 0 === e)) return void eV(1);
              if (e === r - 1) return void eV(-1);
              let i = { from: r, to: e, progress: 0 };
              ((eo.current = i),
                (ep.current = a.Ay.to(i, {
                  progress: 1,
                  duration: 1.08,
                  ease: "power3.inOut",
                  overwrite: !0,
                  onUpdate: () => {
                    let t = i.progress >= 0.5 ? e : r;
                    z((e) => (e === t ? e : t));
                  },
                  onComplete: () => {
                    ((ea.current.value = e), (eo.current = null), z(e));
                  },
                })));
            },
            [k, O, R, eV],
          );
        ((0, o.useEffect)(() => {
          if (!P) return;
          let e = (e) => {
            var t;
            if (
              (e.preventDefault(),
              e.stopPropagation(),
              e.stopImmediatePropagation(),
              !O || R)
            )
              return;
            let n = eb.current,
              r =
                1 === e.deltaMode
                  ? 16
                  : 2 === e.deltaMode
                    ? null != (t = null == n ? void 0 : n.clientHeight)
                      ? t
                      : window.innerHeight
                    : 1,
              i = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
            if (((eh.current += i * r), 65 > Math.abs(eh.current))) return;
            let l = Math.sign(eh.current);
            ((eh.current = 0), eV(l));
          };
          return (
            window.addEventListener("wheel", e, { capture: !0, passive: !1 }),
            () => {
              window.removeEventListener("wheel", e, !0);
            }
          );
        }, [P, O, R, eV, eb]),
          (0, o.useEffect)(() => {
            if (!P) return;
            let e = (e) => {
              ("Escape" === e.key && e_(),
                ("ArrowDown" === e.key || "ArrowRight" === e.key) &&
                  (e.preventDefault(), eV(1)),
                ("ArrowUp" === e.key || "ArrowLeft" === e.key) &&
                  (e.preventDefault(), eV(-1)));
            };
            return (
              window.addEventListener("keydown", e),
              () => {
                window.removeEventListener("keydown", e);
              }
            );
          }, [P, e_, eV]),
          (0, o.useEffect)(() => {
            (ek || eL) && T(!1);
          }, [ek, eL]),
          (0, o.useEffect)(
            () => () => {
              var e, t, n;
              (null == (e = ep.current) || e.kill(),
                null == (t = ev.current) || t.kill(),
                null == (n = _.current) || n.kill());
            },
            [],
          ));
        let eK = eU ? (null == (t = m[eU.index]) ? void 0 : t.title) : null,
          eJ = ek
            ? (null == (u = m[ek.index]) || null == (n = u.title)
                ? void 0
                : n.trim()) || "Untitled"
            : null,
          eQ = ek ? m[ek.index] : null,
          eZ = eQ
            ? 1 +
              (null != (p = eQ.images) ? p : []).filter(
                (e) => e && e !== eQ.src,
              ).length +
              +(null != (s = eQ.srcVideo) && !!s.trim())
            : 0;
        (0, o.useEffect)(() => {
          if (!ek) {
            (W(!1), X(0));
            return;
          }
          let e = 0,
            t = () => {
              let n = G.current,
                r = n
                  ? n.progress >= 0.5
                    ? n.to
                    : n.from
                  : Math.max(0, Math.min(eZ - 1, Math.round(eA.current.value)));
              (X((e) => (e === r ? e : r)),
                (e = window.requestAnimationFrame(t)));
            };
          return (t(), () => window.cancelAnimationFrame(e));
        }, [ek, eZ, eA]);
        let e0 = (0, o.useCallback)(
          (e) => {
            var t;
            if (
              !ek ||
              eL ||
              !ez ||
              (null == (t = _.current) ? void 0 : t.isActive()) ||
              e < 0 ||
              e >= eZ
            )
              return;
            let n = Math.max(0, Math.min(eZ - 1, Math.round(eA.current.value)));
            if (n === e || a.Ay.isTweening(eA.current)) return;
            if (1 === Math.abs(e - n)) {
              _.current = a.Ay.to(eA.current, {
                value: e,
                duration: 1.08,
                ease: "power3.inOut",
                overwrite: !0,
              });
              return;
            }
            let r = { from: n, to: e, progress: 0 };
            ((G.current = r),
              (_.current = a.Ay.to(r, {
                progress: 1,
                duration: 1.08,
                ease: "power3.inOut",
                overwrite: !0,
                onComplete: () => {
                  ((eA.current.value = e), (G.current = null), X(e));
                },
              })));
          },
          [ek, eL, ez, eZ, eA],
        );
        (0, o.useEffect)(() => {
          var e;
          if (ek && !eL) return;
          (null == (e = _.current) || e.kill(), (_.current = null));
          let t = G.current;
          (t &&
            ((eA.current.value = t.progress >= 0.5 ? t.to : t.from),
            (G.current = null)),
            W(!1));
        }, [ek, eL, eA]);
        let e1 =
            null != (v = null == (d = E[L]) ? void 0 : d.discipline) ? v : null,
          e2 = !!(ek && ez && !eL),
          e5 = k && O && !R;
        return (0, r.jsxs)("section", {
          ref: eb,
          onPointerDownCapture: (e) => {
            var t, n;
            if (
              ((eP.current = null),
              (eC.current = null),
              ek ||
                eL ||
                P ||
                ("mouse" === e.pointerType && 0 !== e.button) ||
                e.target.closest("button"))
            )
              return;
            let r =
              null !=
              (n =
                null == (t = ex.current)
                  ? void 0
                  : t.call(ex, e.clientX, e.clientY, !0))
                ? n
                : null;
            ((eP.current = r), (eC.current = r));
          },
          onPointerDown: eD,
          onPointerMove: (e) => {
            var t;
            if ((eH(e), "mouse" === e.pointerType)) {
              if (
                ((eg.current = { x: e.clientX, y: e.clientY }), ek || eL || P)
              )
                return void T(!1);
              T(
                !!(null == (t = ex.current)
                  ? void 0
                  : t.call(ex, e.clientX, e.clientY)),
              );
            }
          },
          onWheelCapture: (e) => {
            G.current && (e.preventDefault(), e.stopPropagation());
          },
          onPointerUp: eF,
          onPointerCancel: () => {
            (eW(), T(!1));
          },
          onPointerLeave: () => {
            ((eg.current = null), T(!1));
          },
          className:
            "relative h-svh w-full touch-none overflow-hidden bg-transparent "
              .concat(ek || P ? "z-[500]" : "", " ")
              .concat(
                ek
                  ? ez && !eL
                    ? "cursor-none"
                    : "cursor-default"
                  : P
                    ? "cursor-default"
                    : j
                      ? "cursor-pointer"
                      : "cursor-default",
              ),
          children: [
            (0, r.jsx)($.A, { threeReady: q, onRevealStart: ee }),
            (0, r.jsx)(g, { backdropRef: eM }),
            (0, r.jsx)(es, { visible: J && !ek && !eL && !P }),
            (0, r.jsxs)(i.Hl, {
              className: "!absolute !inset-0 !z-10",
              camera: { position: [0, 0, 1200], fov: 38, near: 0.1, far: 2e4 },
              dpr: [1, 1.5],
              gl: {
                antialias: !0,
                alpha: !0,
                powerPreference: "high-performance",
              },
              children: [
                (0, r.jsx)(x, {}),
                (0, r.jsxs)(o.Suspense, {
                  fallback: null,
                  children: [
                    (0, r.jsx)(f, {
                      projects: m,
                      scrollTarget: ej,
                      selected: ek,
                      progress: eS,
                      onHoverChange: eY,
                      pressedPlaneRef: eC,
                      titleRef: eT,
                      closingRef: eE,
                      profileActive: P,
                      backdropRef: eM,
                      imageProgress: eA,
                      mediaJump: G,
                      coverMorph: eO,
                      imageHitTestRef: ef,
                      listHitTestRef: ex,
                      pointerPositionRef: eg,
                      initialProjectIndex: er.current,
                    }),
                    (0, r.jsx)(B, {
                      open: k,
                      projectSelected: !!ek,
                      mediaProgress: ea,
                      mediaJump: eo,
                      coverReturn: eu,
                      isOverImage: em,
                      onReadyChange: U,
                      onClosed: eX,
                      htmlBackdropRef: eM,
                    }),
                    (0, r.jsx)($.m, { onReady: et }),
                    " ",
                    (0, r.jsx)(Z, { start: J }),
                  ],
                }),
              ],
            }),
            (0, r.jsx)(ei, { visible: J && !ek && !eL && !P }),
            !ek &&
              !P &&
              (0, r.jsx)("button", {
                type: "button",
                onClick: eq,
                "aria-label": "Open Rustam Kerimov profile",
                className:
                  "absolute right-[5%] top-[225px] z-30 aspect-[4/5] w-[clamp(104px,28vw,140px)] cursor-pointer bg-transparent lg:right-[3.1%] lg:top-[150px] lg:w-[clamp(150px,12vw,210px)]",
              }),
            (0, r.jsx)("div", {
              className:
                "pointer-events-none absolute inset-0 z-[40] transition-opacity duration-200 ease-out",
              style: { opacity: ek || P ? 0 : 1 },
              "aria-hidden": null !== ek || P,
              children: (0, r.jsx)(w, {
                titleRef: eT,
                title: null != (h = null != eJ ? eJ : eK) ? h : "",
              }),
            }),
            (0, r.jsx)(N, {
              selected: ek,
              closing: eL,
              ready: ez,
              project: eQ,
              currentMediaIndex: Y,
              mediaCount: eZ,
              onSelectMedia: e0,
              onMenuHoverChange: W,
            }),
            P &&
              (0, r.jsx)("button", {
                type: "button",
                "aria-label": "Next image or close profile",
                onClick: (e) => {
                  var t;
                  k &&
                    O &&
                    !R &&
                    ((
                      null == (t = em.current)
                        ? void 0
                        : t.call(em, e.clientX, e.clientY)
                    )
                      ? eV(1)
                      : e_());
                },
                className:
                  "absolute inset-0 z-[35] cursor-default bg-transparent",
              }),
            (0, r.jsx)(V, {
              visible: k && O && !R,
              mediaIndex: L,
              activeDiscipline: e1,
              onSelectMedia: e$,
              onMenuHoverChange: H,
            }),
            (e2 || e5) &&
              (0, r.jsx)(
                I,
                {
                  active: !0,
                  hasMultipleMedia: e5 ? E.length > 1 : eZ > 1,
                  isOverImage: e5 ? em : ef,
                  initialMousePosition: eg,
                  menuHovered: e5 ? D : F,
                },
                e5 ? "profile" : "project",
              ),
          ],
        });
      }
    },
  },
]);
