(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
  [177],
  {
    347: () => {},
    4422: (n, e, t) => {
      (Promise.resolve().then(t.bind(t, 3568)),
        Promise.resolve().then(t.t.bind(t, 347, 23)),
        Promise.resolve().then(t.bind(t, 7689)),
        Promise.resolve().then(t.bind(t, 6411)),
        Promise.resolve().then(t.bind(t, 5883)),
        Promise.resolve().then(t.bind(t, 5411)));
    },
    5411: (n, e, t) => {
      "use strict";
      t.d(e, { ProjectNavProvider: () => i });
      var r = t(5155),
        a = t(2115);
      let o = (0, a.createContext)(null),
        i = (n) => {
          let { children: e } = n,
            [t, i] = (0, a.useState)(null);
          return (0, r.jsx)(o.Provider, {
            value: { projectTitle: t, setProjectTitle: i },
            children: e,
          });
        };
    },
    5883: (n, e, t) => {
      "use strict";
      t.d(e, { default: () => u });
      var r = t(5155),
        a = t(2115),
        o = t(6799),
        i = t(5695);
      let s = [0.16, 1, 0.3, 1],
        l = (n) => n.replace(/\/+$/, "") || "/";
      function c(n) {
        let { children: e, delay: t = 0, className: a = "" } = n;
        return (0, r.jsx)(o.P.div, {
          initial: { opacity: 0, y: 14 },
          animate: { opacity: 1, y: 0 },
          transition: { duration: 0.85, delay: t, ease: s },
          className: a,
          children: e,
        });
      }
      function u() {
        let n = (0, i.usePathname)(),
          [e, t] = (0, a.useState)(() => l(n)),
          [o, s] = (0, a.useState)("idle"),
          u = (0, a.useRef)(null);
        ((0, a.useEffect)(() => {
          t(l(n));
        }, [n]),
          (0, a.useEffect)(() => {
            let n = () => t(l(window.location.pathname));
            return (
              window.addEventListener("popstate", n),
              () => {
                window.removeEventListener("popstate", n);
              }
            );
          }, []),
          (0, a.useEffect)(
            () => () => {
              u.current && clearTimeout(u.current);
            },
            [],
          ));
        let d = async () => {
            try {
              (await navigator.clipboard.writeText("rustam-98@hotmail.com"),
                s("copied"));
            } catch (n) {
              s("error");
            }
            (u.current && clearTimeout(u.current),
              (u.current = setTimeout(() => {
                s("idle");
              }, 2200)));
          },
          p = (n) => {
            let e = l(n);
            (l(window.location.pathname) !== e &&
              window.history.pushState(null, "", e),
              t(e),
              window.dispatchEvent(new PopStateEvent("popstate")));
          },
          m = () => {
            window.matchMedia("(max-width: 1023px)").matches
              ? p("/" === e ? "/about" : "/")
              : window.dispatchEvent(new Event("rustam:open-profile"));
          };
        return (0, r.jsx)("nav", {
          "aria-label": "Main navigation",
          className:
            "fixed inset-x-0 top-0 z-[100] w-full bg-transparent px-[5%] pb-4 pt-6 text-color lg:bg-transparent lg:px-[3.1%] lg:pb-0 lg:pt-[18px] lg:text-color",
          children: (0, r.jsxs)("div", {
            className:
              "flex w-full items-start justify-between gap-x-5 ".concat(
                "font-bueno text-[15px] font-medium leading-[1.18] tracking-[-0.025em] lg:text-[clamp(15px,1.1vw,20px)]",
              ),
            children: [
              (0, r.jsxs)(c, {
                delay: 0,
                children: [
                  (0, r.jsx)("button", {
                    type: "button",
                    onClick: () => p("/"),
                    className: "whitespace-nowrap text-left lg:hidden",
                    children: "Rustam Kerimov",
                  }),
                  (0, r.jsxs)("div", {
                    className: "hidden flex-col items-start lg:flex",
                    children: [
                      (0, r.jsx)("span", {
                        className: "text-sm",
                        children: "Name:",
                      }),
                      (0, r.jsx)("span", {
                        className: "whitespace-nowrap",
                        children: "Rustam Kerimov",
                      }),
                    ],
                  }),
                ],
              }),
              (0, r.jsx)(c, {
                delay: 0.08,
                className: "hidden lg:block",
                children: (0, r.jsxs)("div", {
                  className: "flex flex-col items-start",
                  children: [
                    (0, r.jsx)("span", {
                      className: "text-sm",
                      children: "occupation:",
                    }),
                    (0, r.jsx)("span", {
                      className: "whitespace-nowrap",
                      children: "Graphic Designer",
                    }),
                  ],
                }),
              }),
              (0, r.jsx)(c, {
                delay: 0.16,
                className: "hidden lg:block",
                children: (0, r.jsxs)("div", {
                  className: "flex flex-col items-start",
                  children: [
                    (0, r.jsx)("span", {
                      className: "text-sm",
                      children: "Location:",
                    }),
                    "Oslo, Norway",
                  ],
                }),
              }),
              (0, r.jsx)(c, {
                delay: 0.24,
                className: "hidden lg:block",
                children: (0, r.jsxs)("div", {
                  className: "flex flex-col items-start",
                  children: [
                    (0, r.jsx)("span", {
                      className: "text-sm",
                      children: "Connect:",
                    }),
                    (0, r.jsx)("button", {
                      type: "button",
                      onClick: d,
                      className:
                        "whitespace-nowrap cursor-pointer text-left transition-opacity duration-300 hover:opacity-50",
                      "aria-label": "Copy email address",
                      children: (0, r.jsx)("span", {
                        "aria-live": "polite",
                        children:
                          "copied" === o
                            ? "Copied!"
                            : "error" === o
                              ? "Copy failed"
                              : "Copy Email",
                      }),
                    }),
                    (0, r.jsx)("a", {
                      href: "https://www.instagram.com/kerimov.designs/",
                      target: "_blank",
                      rel: "noopener noreferrer",
                      className:
                        "whitespace-nowrap transition-opacity duration-300 hover:opacity-50",
                      children: "Instagram",
                    }),
                    (0, r.jsx)("a", {
                      href: "https://www.linkedin.com/in/rustam-kerimov-75bb5a331/",
                      target: "_blank",
                      rel: "noopener noreferrer",
                      className:
                        "whitespace-nowrap transition-opacity duration-300 hover:opacity-50",
                      children: "LinkedIn",
                    }),
                  ],
                }),
              }),
              (0, r.jsx)(c, {
                delay: 0.32,
                children: (0, r.jsxs)("div", {
                  className: "flex flex-col items-start text-left",
                  children: [
                    (0, r.jsx)("button", {
                      type: "button",
                      onClick: m,
                      className:
                        "cursor-pointer whitespace-nowrap transition-opacity duration-300 hover:opacity-50 lg:hidden",
                      children: "/" === e ? "About me" : "Back",
                    }),
                    (0, r.jsx)("span", {
                      className: "hidden text-sm lg:block",
                      children: "Profile:",
                    }),
                    (0, r.jsx)("button", {
                      type: "button",
                      onClick: m,
                      className:
                        "hidden cursor-pointer whitespace-nowrap text-left transition-opacity duration-300 hover:opacity-50 lg:block",
                      children: "About me",
                    }),
                  ],
                }),
              }),
            ],
          }),
        });
      }
    },
    6411: (n, e, t) => {
      "use strict";
      t.d(e, { HeroIntroProvider: () => i });
      var r = t(5155),
        a = t(2115);
      let o = (0, a.createContext)(null);
      function i(n) {
        let { children: e } = n,
          [t, i] = (0, a.useState)(!1);
        return (0, r.jsx)(o.Provider, {
          value: { introExited: t, setIntroExited: i },
          children: e,
        });
      }
    },
    7689: (n, e, t) => {
      "use strict";
      t.d(e, { default: () => h, w: () => f });
      var r = t(5155),
        a = t(2115),
        o = t(3084),
        i = t(5695),
        s = t(3967),
        l = t(7558),
        c = t(3264);
      function u(n) {
        let {
            status: e,
            variant: t,
            color: o,
            onCovered: i,
            onFinished: l,
          } = n,
          u = (0, a.useRef)(null),
          { viewport: d } = (0, s.A)(),
          p = (0, a.useRef)(+("leaving" === e)),
          m = (0, a.useRef)({
            from: +("leaving" === e),
            to: +("leaving" !== e),
            elapsed: 0,
            completed: !1,
          }),
          f = (0, a.useMemo)(
            () =>
              (function (n, e) {
                let t = (null == e ? void 0 : e.trim()) || "";
                if (/^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.test(t)) {
                  let n = new c.Q1f(t),
                    e = new c.Q1f("#2f302d"),
                    r = new c.Q1f("#4a4944");
                  return {
                    a: n.clone().lerp(e, 0.52),
                    b: n.clone().lerp(r, 0.38),
                  };
                }
                return "projectDetails" === n
                  ? { a: new c.Q1f("#11130f"), b: new c.Q1f("#1e211c") }
                  : { a: new c.Q1f("#31362f"), b: new c.Q1f("#545c51") };
              })(t, o),
            [t, o],
          ),
          h = (0, a.useMemo)(
            () => ({
              uTime: { value: 0 },
              uProgress: { value: p.current },
              uColorA: { value: f.a },
              uColorB: { value: f.b },
            }),
            [f],
          );
        return (
          (0, a.useEffect)(() => {
            m.current = {
              from: p.current,
              to: +("entering" === e),
              elapsed: 0,
              completed: !1,
            };
          }, [e]),
          (0, a.useEffect)(() => {
            let n = u.current;
            n &&
              (n.uniforms.uColorA.value.copy(f.a),
              n.uniforms.uColorB.value.copy(f.b));
          }, [f]),
          (0, s.C)((n, t) => {
            let r = u.current;
            if (!r) return;
            let a = Math.min(t, 1 / 30);
            r.uniforms.uTime.value = n.clock.elapsedTime;
            let o = m.current;
            if (o.completed) return;
            o.elapsed += a;
            let s = "entering" === e ? 0.82 : 0.68,
              d = c.cj9.clamp(o.elapsed / s, 0, 1),
              f = -(Math.cos(Math.PI * d) - 1) / 2,
              h = c.cj9.lerp(o.from, o.to, f);
            if (((p.current = h), (r.uniforms.uProgress.value = h), !(d < 1))) {
              if (
                ((o.completed = !0),
                (p.current = o.to),
                (r.uniforms.uProgress.value = o.to),
                "entering" === e)
              )
                return void i();
              l();
            }
          }),
          (0, r.jsxs)("mesh", {
            children: [
              (0, r.jsx)("planeGeometry", {
                args: [1.02 * d.width, 1.02 * d.height],
              }),
              (0, r.jsx)("shaderMaterial", {
                ref: u,
                uniforms: h,
                vertexShader:
                  "\n  varying vec2 vUv;\n\n  void main() {\n    vUv = uv;\n\n    gl_Position =\n      projectionMatrix *\n      modelViewMatrix *\n      vec4(position, 1.0);\n  }\n",
                fragmentShader:
                  "\n  precision highp float;\n\n  uniform float uTime;\n  uniform float uProgress;\n\n  uniform vec3 uColorA;\n  uniform vec3 uColorB;\n\n  varying vec2 vUv;\n\n  \n  float hash(vec2 p) {\n    p = fract(\n      p * vec2(\n        123.34,\n        456.21\n      )\n    );\n\n    p += dot(\n      p,\n      p + 45.32\n    );\n\n    return fract(\n      p.x * p.y\n    );\n  }\n\n \n\n  float noise(vec2 p) {\n    vec2 i = floor(p);\n    vec2 f = fract(p);\n\n    f =\n      f *\n      f *\n      (\n        3.0 -\n        2.0 * f\n      );\n\n    float a =\n      hash(i);\n\n    float b =\n      hash(\n        i +\n        vec2(1.0, 0.0)\n      );\n\n    float c =\n      hash(\n        i +\n        vec2(0.0, 1.0)\n      );\n\n    float d =\n      hash(\n        i +\n        vec2(1.0, 1.0)\n      );\n\n    return mix(\n      mix(\n        a,\n        b,\n        f.x\n      ),\n      mix(\n        c,\n        d,\n        f.x\n      ),\n      f.y\n    );\n  }\n\n \n\n  float fbm(vec2 p) {\n    float value = 0.0;\n    float amplitude = 0.5;\n\n    mat2 rotation = mat2(\n      0.86,\n      -0.50,\n      0.50,\n      0.86\n    );\n\n    for (\n      int i = 0;\n      i < 4;\n      i++\n    ) {\n      value +=\n        noise(p) *\n        amplitude;\n\n      p =\n        rotation *\n        p *\n        1.82;\n\n      amplitude *=\n        0.48;\n    }\n\n    return value;\n  }\n\n  \n\n  void main() {\n    vec2 uv = vUv;\n\n\n    vec2 cloudUv =\n      uv * vec2(\n        2.15,\n        2.35\n      );\n\n    cloudUv.x +=\n      sin(\n        uv.y * 3.0 +\n        uTime * 0.12\n      ) *\n      0.055;\n\n    cloudUv.y +=\n      cos(\n        uv.x * 2.6 -\n        uTime * 0.095\n      ) *\n      0.045;\n\n    float cloudA =\n      fbm(\n        cloudUv +\n        vec2(\n          uTime * 0.014,\n          -uTime * 0.010\n        )\n      );\n\n \n\n    vec2 secondUv =\n      uv * vec2(\n        1.45,\n        1.65\n      );\n\n    secondUv +=\n      vec2(\n        -uTime * 0.009,\n        uTime * 0.007\n      );\n\n    float cloudB =\n      fbm(\n        secondUv\n      );\n\n    float field =\n      mix(\n        cloudA,\n        cloudB,\n        0.28\n      );\n\n    field =\n      smoothstep(\n        0.16,\n        0.84,\n        field\n      );\n\n \n\n    float threshold =\n      mix(\n        -0.18,\n        1.18,\n        uProgress\n      );\n\n    float softness =\n      0.16;\n\n    float mask =\n      1.0 -\n      smoothstep(\n        threshold - softness,\n        threshold + softness,\n        field\n      );\n\n \n\n    float edgeDistance =\n      abs(\n        field -\n        threshold\n      );\n\n    float edgeArea =\n      1.0 -\n      smoothstep(\n        0.0,\n        0.24,\n        edgeDistance\n      );\n\n    float secondary =\n      fbm(\n        uv * 3.0 +\n        vec2(\n          -uTime * 0.012,\n          uTime * 0.009\n        )\n      );\n\n    mask +=\n      (\n        secondary -\n        0.5\n      ) *\n      edgeArea *\n      0.11;\n\n    mask =\n      clamp(\n        mask,\n        0.0,\n        1.0\n      );\n\n  \n\n    mask *=\n      smoothstep(\n        0.0,\n        0.045,\n        uProgress\n      );\n\n   \n    mask =\n      mix(\n        mask,\n        1.0,\n        smoothstep(\n          0.955,\n          1.0,\n          uProgress\n        )\n      );\n\n  \n\n    float baseVariation =\n      smoothstep(\n        0.18,\n        0.82,\n        cloudB\n      );\n\n    vec3 color =\n      mix(\n        uColorA,\n        uColorB,\n        baseVariation * 0.42\n      );\n\n    \n\n    float greenField =\n      fbm(\n        uv * 1.25 +\n        vec2(\n          uTime * 0.004,\n          -uTime * 0.003\n        )\n      );\n\n    greenField =\n      smoothstep(\n        0.20,\n        0.80,\n        greenField\n      );\n\n    \n\n    vec3 oliveTint =\n      vec3(\n        0.22,\n        0.27,\n        0.20\n      );\n\n   \n\n    color =\n      mix(\n        color,\n        oliveTint,\n        greenField * 0.09\n      );\n\n   \n    color +=\n      (\n        cloudA -\n        0.5\n      ) *\n      0.012;\n\n    gl_FragColor =\n      vec4(\n        color,\n        mask\n      );\n\n    #include <colorspace_fragment>\n  }\n",
                transparent: !0,
                depthWrite: !1,
                depthTest: !1,
                toneMapped: !1,
                precision: "highp",
              }),
            ],
          })
        );
      }
      function d(n) {
        let {
          status: e,
          variant: t,
          color: a,
          onCovered: o,
          onFinished: i,
        } = n;
        return (0, r.jsx)("div", {
          "aria-hidden": "true",
          className:
            " pointer-events-none fixed inset-0 z-[99999] overflow-hidden ",
          children: (0, r.jsx)(l.Hl, {
            orthographic: !0,
            camera: { position: [0, 0, 5], zoom: 100, near: 0.01, far: 20 },
            dpr: [1, 1.25],
            frameloop: "always",
            gl: {
              antialias: !1,
              alpha: !0,
              depth: !1,
              stencil: !1,
              powerPreference: "high-performance",
            },
            children: (0, r.jsx)(u, {
              status: e,
              variant: t,
              color: a,
              onCovered: o,
              onFinished: i,
            }),
          }),
        });
      }
      let p = (0, a.createContext)(null),
        m = { status: "idle", variant: "destination", color: null };
      function f() {
        let n = (0, a.useContext)(p);
        if (!n)
          throw Error(
            "usePageTransition must be used inside ClientPageTransitionWrapper",
          );
        return n;
      }
      function h(n) {
        let { children: e } = n,
          t = (0, i.useRouter)(),
          s = (0, i.usePathname)(),
          l = (0, o.I)(),
          [c, u] = (0, a.useState)(m),
          f = (0, a.useRef)(s),
          h = (0, a.useRef)(null),
          v = (0, a.useRef)("idle"),
          x = (0, a.useRef)(!1),
          g = "idle" !== c.status,
          w = (0, a.useCallback)(
            function (n, e) {
              arguments.length > 2 && void 0 !== arguments[2] && arguments[2];
              let r = arguments.length > 3 ? arguments[3] : void 0;
              if (n && n !== s && "idle" === v.current) {
                if (l) return void t.push(n);
                ((v.current = "entering"),
                  (h.current = n),
                  (x.current = !1),
                  t.prefetch(n),
                  u({
                    status: "entering",
                    variant: n
                      .split("?")[0]
                      .split("#")[0]
                      .startsWith("/project/")
                      ? "projectDetails"
                      : "destination",
                    color: (null == r ? void 0 : r.trim()) || null,
                  }));
              }
            },
            [s, t, l],
          ),
          b = (0, a.useCallback)(() => {
            if ("entering" !== v.current || x.current) return;
            let n = h.current;
            n && ((x.current = !0), t.push(n));
          }, [t]);
        (0, a.useEffect)(() => {
          s !== f.current &&
            ((f.current = s),
            h.current &&
              ((v.current = "leaving"),
              u((n) => ({ ...n, status: "leaving" }))));
        }, [s]);
        let j = (0, a.useCallback)(() => {
            "leaving" === v.current &&
              ((v.current = "idle"),
              (h.current = null),
              (x.current = !1),
              u(m));
          }, []),
          y = (0, a.useMemo)(
            () => ({ startTransition: w, isTransitioning: g }),
            [w, g],
          );
        return (0, r.jsxs)(p.Provider, {
          value: y,
          children: [
            e,
            g && !l
              ? (0, r.jsx)(d, {
                  status: c.status,
                  variant: c.variant,
                  color: c.color,
                  onCovered: b,
                  onFinished: j,
                })
              : null,
          ],
        });
      }
    },
  },
  (n) => {
    var e = (e) => n((n.s = e));
    (n.O(0, [690, 831, 367, 529, 799, 204, 997, 441, 684, 358], () => e(4422)),
      (_N_E = n.O()));
  },
]);
