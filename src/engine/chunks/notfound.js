(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
  [345],
  {
    6654: (e, t, n) => {
      "use strict";
      (Object.defineProperty(t, "__esModule", { value: !0 }),
        Object.defineProperty(t, "useMergedRef", {
          enumerable: !0,
          get: function () {
            return l;
          },
        }));
      let i = n(2115);
      function l(e, t) {
        let n = (0, i.useRef)(null),
          l = (0, i.useRef)(null);
        return (0, i.useCallback)(
          (i) => {
            if (null === i) {
              let e = n.current;
              e && ((n.current = null), e());
              let t = l.current;
              t && ((l.current = null), t());
            } else (e && (n.current = r(e, i)), t && (l.current = r(t, i)));
          },
          [e, t],
        );
      }
      function r(e, t) {
        if ("function" != typeof e)
          return (
            (e.current = t),
            () => {
              e.current = null;
            }
          );
        {
          let n = e(t);
          return "function" == typeof n ? n : () => e(null);
        }
      }
      ("function" == typeof t.default ||
        ("object" == typeof t.default && null !== t.default)) &&
        void 0 === t.default.__esModule &&
        (Object.defineProperty(t.default, "__esModule", { value: !0 }),
        Object.assign(t.default, t),
        (e.exports = t.default));
    },
    9007: (e, t, n) => {
      (Promise.resolve().then(n.t.bind(n, 6874, 23)),
        Promise.resolve().then(n.bind(n, 9812)));
    },
    9812: (e, t, n) => {
      "use strict";
      n.d(t, { default: () => d });
      var i = n(5155),
        l = n(2115),
        r = n(3264),
        o = n(7431);
      let a = ["4", "0", "4"];
      function s(e) {
        let t = e < 768;
        return {
          cameraZ: t ? 5.8 : 7,
          digitSize: t ? 1.1 : 1.65,
          floatStrength: t ? 0.12 : 0.28,
          finalPositions: [
            new r.Pq0(t ? -0.82 : -1.25, 0, 0),
            new r.Pq0(0, 0, 0),
            new r.Pq0(t ? 0.82 : 1.25, 0, 0),
          ],
          orbitOffsets: [
            new r.Pq0(t ? -0.98 : -1.6, 0.32, -0.2),
            new r.Pq0(0, -0.32, 0.2),
            new r.Pq0(t ? 0.98 : 1.6, 0.32, -0.2),
          ],
        };
      }
      function d() {
        let e = (0, l.useRef)(null);
        return (
          (0, l.useEffect)(() => {
            let t = e.current;
            if (null === t) return;
            let n = s(window.innerWidth),
              i = new r.Z58(),
              l = new r.ubm(45, t.clientWidth / t.clientHeight, 0.1, 100);
            l.position.z = n.cameraZ;
            let d = new o.WebGLRenderer({ alpha: !0, antialias: !0 });
            (d.setPixelRatio(Math.min(window.devicePixelRatio, 2)),
              d.setSize(t.clientWidth, t.clientHeight),
              t.appendChild(d.domElement));
            let u = new r.YJl();
            i.add(u);
            let c = a.map((e, t) => {
                let i = (function (e) {
                    let t = document.createElement("canvas");
                    ((t.width = 512), (t.height = 512));
                    let n = t.getContext("2d");
                    if (null === n) return null;
                    (n.clearRect(0, 0, t.width, t.height),
                      (n.fillStyle = "white"),
                      (n.font = "900 380px Arial, Helvetica, sans-serif"),
                      (n.textAlign = "center"),
                      (n.textBaseline = "middle"),
                      n.fillText(e, t.width / 2, t.height / 2 + 18));
                    let i = new r.GOR(t);
                    return ((i.needsUpdate = !0), (i.colorSpace = r.er$), i);
                  })(e),
                  l = new r.V9B({
                    map: null != i ? i : void 0,
                    transparent: !0,
                    opacity: 0.95,
                    side: r.$EB,
                    depthWrite: !1,
                  }),
                  o = new r.bdM(n.digitSize, n.digitSize),
                  a = new r.eaF(o, l);
                return (a.position.copy(n.orbitOffsets[t]), u.add(a), a);
              }),
              f = new r.zD7(),
              h = [0.9, -1.35, 1.15];
            function p(e, t, n) {
              let i = Math.min(1, Math.max(0, (n - e) / (t - e)));
              return i * i * (3 - 2 * i);
            }
            let w = 0;
            function m() {
              ((n = s(window.innerWidth)),
                (l.aspect = t.clientWidth / t.clientHeight),
                (l.position.z = n.cameraZ),
                l.updateProjectionMatrix(),
                d.setSize(t.clientWidth, t.clientHeight),
                d.setPixelRatio(Math.min(window.devicePixelRatio, 2)),
                c.forEach((e) => {
                  (e.geometry.dispose(),
                    (e.geometry = new r.bdM(n.digitSize, n.digitSize)));
                }));
            }
            return (
              window.addEventListener("resize", m),
              !(function e() {
                let t = f.getElapsedTime(),
                  r = (t % 6.5) / 6.5,
                  o = p(0.48, 0.72, r) * (1 - p(0.82, 1, r));
                (c.forEach((e, i) => {
                  let l = n.orbitOffsets[i].clone();
                  ((l.x += Math.sin(t * (0.7 + 0.25 * i)) * n.floatStrength),
                    (l.y += Math.cos(t * (0.9 + 0.2 * i)) * n.floatStrength),
                    (l.z +=
                      Math.sin(t * (0.6 + 0.3 * i)) * n.floatStrength * 0.6),
                    e.position.lerpVectors(l, n.finalPositions[i], o),
                    (e.rotation.y = t * h[i] * (1 - o)),
                    (e.rotation.x =
                      0.35 * Math.sin(t * (0.8 + 0.2 * i)) * (1 - o)),
                    (e.rotation.z =
                      0.18 * Math.sin(t * (0.6 + 0.15 * i)) * (1 - o)),
                    e.scale.setScalar(1 + 0.35 * o));
                }),
                  (u.rotation.z = 0.04 * Math.sin(0.18 * t) * (1 - o)),
                  d.render(i, l),
                  (w = window.requestAnimationFrame(e)));
              })(),
              () => {
                (window.cancelAnimationFrame(w),
                  window.removeEventListener("resize", m),
                  c.forEach((e) => {
                    var t;
                    (e.geometry.dispose(),
                      null == (t = e.material.map) || t.dispose(),
                      e.material.dispose());
                  }),
                  d.dispose(),
                  d.domElement.parentElement === t &&
                    t.removeChild(d.domElement));
              }
            );
          }, []),
          (0, i.jsx)("div", {
            ref: e,
            className: "pointer-events-none absolute inset-0",
            "aria-hidden": "true",
          })
        );
      }
    },
  },
  (e) => {
    var t = (t) => e((e.s = t));
    (e.O(0, [831, 367, 874, 441, 684, 358], () => t(9007)), (_N_E = e.O()));
  },
]);
