(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
  [924],
  {
    255: (e, t, n) => {
      "use strict";
      function r(e) {
        let { moduleIds: t } = e;
        return null;
      }
      (Object.defineProperty(t, "__esModule", { value: !0 }),
        Object.defineProperty(t, "PreloadChunks", {
          enumerable: !0,
          get: function () {
            return r;
          },
        }),
        n(5155),
        n(7650),
        n(5744),
        n(589));
    },
    613: (e, t, n) => {
      "use strict";
      n.d(t, { default: () => s });
      var r = n(5155),
        a = n(2115),
        i = n(2810);
      let l = (0, a.createContext)(null);
      function s(e) {
        let { children: t } = e,
          [n, s] = (0, a.useState)(null);
        return (
          (0, a.useEffect)(() => {
            let e = new i.A();
            s(e);
            let t = requestAnimationFrame(function t(n) {
              (e.raf(n), requestAnimationFrame(t));
            });
            return () => {
              (cancelAnimationFrame(t), e.destroy());
            };
          }, []),
          (0, r.jsx)(l.Provider, { value: n, children: t })
        );
      }
    },
    2146: (e, t, n) => {
      "use strict";
      function r(e) {
        let { reason: t, children: n } = e;
        return n;
      }
      (Object.defineProperty(t, "__esModule", { value: !0 }),
        Object.defineProperty(t, "BailoutToCSR", {
          enumerable: !0,
          get: function () {
            return r;
          },
        }),
        n(5262));
    },
    4054: (e, t) => {
      "use strict";
      (Object.defineProperty(t, "__esModule", { value: !0 }),
        !(function (e, t) {
          for (var n in t)
            Object.defineProperty(e, n, { enumerable: !0, get: t[n] });
        })(t, {
          bindSnapshot: function () {
            return l;
          },
          createAsyncLocalStorage: function () {
            return i;
          },
          createSnapshot: function () {
            return s;
          },
        }));
      let n = Object.defineProperty(
        Error(
          "Invariant: AsyncLocalStorage accessed in runtime where it is not available",
        ),
        "__NEXT_ERROR_CODE",
        { value: "E504", enumerable: !1, configurable: !0 },
      );
      class r {
        disable() {
          throw n;
        }
        getStore() {}
        run() {
          throw n;
        }
        exit() {
          throw n;
        }
        enterWith() {
          throw n;
        }
        static bind(e) {
          return e;
        }
      }
      let a = "undefined" != typeof globalThis && globalThis.AsyncLocalStorage;
      function i() {
        return a ? new a() : new r();
      }
      function l(e) {
        return a ? a.bind(e) : r.bind(e);
      }
      function s() {
        return a
          ? a.snapshot()
          : function (e, ...t) {
              return e(...t);
            };
      }
    },
    4656: (e, t, n) => {
      "use strict";
      n.d(t, { default: () => k });
      var r = n(5155),
        a = n(6645),
        i = n.n(a),
        l = n(2115),
        s = n(5695),
        o = n(3084),
        c = n(6799),
        d = n(4760);
      let u = [0.16, 1, 0.3, 1],
        m = [
          {
            title: "Visual Identities",
            src: "/visual-identity.jpg",
            type: "image",
            description:
              "Building distinctive visual systems that give brands a clear and recognizable voice. From typography and color to composition and visual direction.",
          },
          {
            title: "Logo Design",
            src: "/logo-design.jpg",
            type: "image",
            description:
              "Creating memorable marks that turn ideas into recognizable visual signatures through shape, proportion and typography.",
          },
          {
            title: "Art Direction",
            src: "/art-direction.jpg",
            type: "image",
            description:
              "Shaping visual experiences through a clear creative perspective, connecting imagery, typography and composition.",
          },
          {
            title: "Motion & Animation",
            src: "/bylarm-new.mp4",
            type: "video",
            description:
              "Bringing graphic design to life through movement, rhythm and timing. Exploring how motion adds character and energy to visual communication.",
          },
          {
            title: "Editorial Design",
            src: "/editorial-design.jpg",
            type: "image",
            description:
              "Exploring the relationship between typography, imagery and space to create expressive editorial layouts.",
          },
        ],
        p = (e) => e.replace(/\/+$/, "") || "/";
      function x(e) {
        var t, n;
        let {
            text: a,
            delay: i = 0,
            stagger: l = 0.045,
            className: s = "",
          } = e,
          d = null != (t = (0, o.I)()) && t,
          m = null != (n = a.match(/\S+|\s+/g)) ? n : [];
        return (0, r.jsx)(c.P.span, {
          className: "block whitespace-pre-line ".concat(s),
          initial: "hidden",
          animate: "visible",
          variants: {
            hidden: {},
            visible: {
              transition: {
                delayChildren: d ? 0 : i,
                staggerChildren: d ? 0 : l,
              },
            },
          },
          children: m.map((e, t) =>
            /^\s+$/.test(e)
              ? (0, r.jsx)("span", { children: e }, t)
              : (0, r.jsx)(
                  "span",
                  {
                    className:
                      "inline-block overflow-hidden align-bottom pb-[0.12em] -mb-[0.12em]",
                    children: (0, r.jsx)(c.P.span, {
                      className: "inline-block will-change-transform",
                      variants: {
                        hidden: d
                          ? { opacity: 0 }
                          : { y: "115%", opacity: 0, filter: "blur(3px)" },
                        visible: d
                          ? { opacity: 1, transition: { duration: 0.2 } }
                          : {
                              y: "0%",
                              opacity: 1,
                              filter: "blur(0px)",
                              transition: { duration: 0.75, ease: u },
                            },
                      },
                      children: e,
                    }),
                  },
                  t,
                ),
          ),
        });
      }
      function f(e) {
        let {
          href: t,
          navigate: n,
          children: a,
          className: i = "",
          ariaLabel: l,
        } = e;
        return (0, r.jsx)("a", {
          href: t,
          "aria-label": l,
          className: i,
          onClick: (e) => {
            0 !== e.button ||
              e.metaKey ||
              e.ctrlKey ||
              e.shiftKey ||
              e.altKey ||
              (e.preventDefault(), n(t));
          },
          children: a,
        });
      }
      function h() {
        let [e, t] = (0, l.useState)("idle"),
          n = (0, l.useRef)(null);
        (0, l.useEffect)(
          () => () => {
            n.current && clearTimeout(n.current);
          },
          [],
        );
        let a = async () => {
          try {
            (await navigator.clipboard.writeText("rustam-98@hotmail.com"),
              t("copied"));
          } catch (e) {
            t("error");
          }
          (n.current && clearTimeout(n.current),
            (n.current = setTimeout(() => {
              t("idle");
            }, 2200)));
        };
        return (0, r.jsxs)("footer", {
          className: "pb-12 pt-16 font-bueno",
          children: [
            (0, r.jsxs)("div", {
              className:
                "grid grid-cols-2 gap-x-6 text-[15px] font-medium leading-[1.25]",
              children: [
                (0, r.jsxs)("div", {
                  className: "flex flex-col items-start",
                  children: [
                    (0, r.jsx)("span", {
                      className: "mb-4",
                      children: "Services:",
                    }),
                    m.map((e) =>
                      (0, r.jsx)("span", { children: e.title }, e.title),
                    ),
                  ],
                }),
                (0, r.jsxs)("div", {
                  className: "flex flex-col items-start",
                  children: [
                    (0, r.jsx)("span", {
                      className: "mb-4",
                      children: "Connect:",
                    }),
                    (0, r.jsx)("button", {
                      type: "button",
                      onClick: a,
                      className:
                        "text-left transition-opacity duration-300 hover:opacity-50",
                      children: (0, r.jsx)("span", {
                        "aria-live": "polite",
                        children:
                          "copied" === e
                            ? "Copied!"
                            : "error" === e
                              ? "Copy failed"
                              : "Copy Email",
                      }),
                    }),
                    (0, r.jsx)("a", {
                      href: "https://www.instagram.com/kerimov.designs/",
                      target: "_blank",
                      rel: "noopener noreferrer",
                      className:
                        "transition-opacity duration-300 hover:opacity-50",
                      children: "Instagram",
                    }),
                    (0, r.jsx)("a", {
                      href: "https://www.linkedin.com/in/rustam-kerimov-75bb5a331/",
                      target: "_blank",
                      rel: "noopener noreferrer",
                      className:
                        "transition-opacity duration-300 hover:opacity-50",
                      children: "LinkedIn",
                    }),
                  ],
                }),
              ],
            }),
            (0, r.jsxs)("div", {
              children: [
                (0, r.jsx)("p", {
                  className: "mt-16 text-[13px] font-medium leading-[1.25]",
                  children: "Design / Development:",
                }),
                (0, r.jsx)("a", {
                  href: "https://www.jonasnygaard.com",
                  target: "_blank",
                  rel: "noopener noreferrer",
                  className:
                    "transition-opacity  underline duration-300 hover:opacity-50",
                  children: "Jonas Nygaard",
                }),
              ],
            }),
          ],
        });
      }
      function g(e) {
        let { projects: t, navigate: n } = e;
        return (0, r.jsxs)("section", {
          "aria-labelledby": "mobile-selected-work",
          className: "pb-16",
          children: [
            (0, r.jsx)("h2", {
              id: "mobile-selected-work",
              className:
                "mb-5 font-bueno text-[16px] font-bold  leading-none tracking-[-0.025em]",
              children: "Selected Work:",
            }),
            (0, r.jsx)("div", {
              className: "grid grid-cols-2 items-start gap-x-3 gap-y-8",
              children: t.map((e) =>
                (0, r.jsxs)(
                  f,
                  {
                    href: "/project/".concat(encodeURIComponent(String(e.id))),
                    navigate: n,
                    ariaLabel: "View ".concat(e.title),
                    className: "group block min-w-0 outline-offset-4",
                    children: [
                      (0, r.jsx)("div", {
                        className:
                          "relative aspect-[4/3] w-full overflow-hidden bg-[#1e211b]",
                        children: (0, r.jsx)("img", {
                          src: e.src,
                          alt: e.title,
                          className: "h-full w-full object-cover",
                          loading: "lazy",
                          decoding: "async",
                        }),
                      }),
                      (0, r.jsx)("h3", {
                        className:
                          "mt-2.5 font-bueno text-[12px] font-medium uppercase leading-[1.25] sm:text-[14px]",
                        children: e.title,
                      }),
                    ],
                  },
                  String(e.id),
                ),
              ),
            }),
          ],
        });
      }
      function b(e) {
        let { projects: t, navigate: n } = e;
        return (0, r.jsxs)(r.Fragment, {
          children: [
            (0, r.jsxs)("section", {
              className: "pt-16 sm:pt-20",
              children: [
                (0, r.jsx)("h1", {
                  className:
                    "max-w-[560px] font-bueno text-[clamp(28px,7.3vw,46px)] font-bold uppercase leading-[1.04] tracking-[-0.035em]",
                  children: (0, r.jsx)(x, {
                    text: "Graphic Designer\nCrafting Visual Identities,\nTypography and Motion.",
                    delay: 0.12,
                    stagger: 0.045,
                  }),
                }),
                (0, r.jsx)("div", {
                  className: "mt-9 flex justify-end sm:mt-12",
                  children: (0, r.jsx)(f, {
                    href: "/about",
                    navigate: n,
                    ariaLabel: "About Rustam Kerimov",
                    className: "block w-[48%] max-w-[240px] outline-offset-4",
                    children: (0, r.jsx)("img", {
                      src: "/rk-portrait.jpg",
                      alt: "Portrait of Rustam Kerimov",
                      className: "aspect-[4/5] w-full object-cover",
                      decoding: "async",
                    }),
                  }),
                }),
              ],
            }),
            (0, r.jsx)("div", {
              className: "mt-16 sm:mt-20",
              children: (0, r.jsx)(g, { projects: t, navigate: n }),
            }),
          ],
        });
      }
      function v(e) {
        var t, n, a, i, l, s, o, c, d, u;
        let { project: m } = e,
          p = Array.from(
            new Set(
              [m.src, ...(null != (u = m.images) ? u : [])].filter(
                (e) => "string" == typeof e && !!e.trim(),
              ),
            ),
          ),
          f =
            null !=
            (d = null == (t = m.tags) ? void 0 : t.filter((e) => e.trim()))
              ? d
              : [];
        return (0, r.jsxs)("article", {
          className: "pb-16 pt-14",
          children: [
            (0, r.jsxs)("header", {
              className: "mb-10",
              children: [
                (0, r.jsx)("h1", {
                  className:
                    "max-w-[580px] font-bueno text-[clamp(31px,8vw,54px)] font-bold uppercase leading-[1.02] tracking-[-0.035em]",
                  children: (0, r.jsx)(x, {
                    text: m.title,
                    delay: 0.08,
                    stagger: 0.05,
                  }),
                }),
                f.length > 0 &&
                  (0, r.jsx)("p", {
                    className:
                      "mt-5 font-sans text-[10px] font-medium uppercase leading-[1.6] tracking-[0.1em] text-[#e7e3dd]/90",
                    children: f.join(" / "),
                  }),
              ],
            }),
            (0, r.jsxs)("div", {
              className: "space-y-3",
              children: [
                p.map((e, t) =>
                  (0, r.jsx)(
                    "img",
                    {
                      src: e,
                      alt: "".concat(m.title, " — work ").concat(t + 1),
                      className: "block h-auto w-full bg-[#1e211b]",
                      loading: 0 === t ? "eager" : "lazy",
                      decoding: "async",
                    },
                    e,
                  ),
                ),
                (null == (n = m.srcVideo) ? void 0 : n.trim()) &&
                  (0, r.jsx)("video", {
                    className:
                      "pointer-events-none block h-auto w-full bg-black",
                    autoPlay: !0,
                    muted: !0,
                    loop: !0,
                    playsInline: !0,
                    preload: "auto",
                    disablePictureInPicture: !0,
                    "aria-label": "".concat(m.title, " video"),
                    children: (0, r.jsx)("source", { src: m.srcVideo }),
                  }),
              ],
            }),
            ((null == (a = m.description) ? void 0 : a.trim()) ||
              (null == (i = m.type) ? void 0 : i.trim()) ||
              (null == (l = m.tools) ? void 0 : l.trim())) &&
              (0, r.jsxs)("div", {
                className:
                  "mt-12 grid grid-cols-2 gap-x-5 gap-y-9 border-t border-[#e7e3dd]/20 pt-7",
                children: [
                  (null == (s = m.description) ? void 0 : s.trim()) &&
                    (0, r.jsxs)("div", {
                      className: "col-span-2",
                      children: [
                        (0, r.jsx)("p", {
                          className:
                            "mb-3  text-[12px]  tracking-[0.14em] text-[#e7e3dd]",
                          children: "About the project:",
                        }),
                        (0, r.jsx)("p", {
                          className:
                            "whitespace-pre-line font-bueno text-[17px] leading-[1.45] text-[#e7e3dd]/85",
                          children: m.description,
                        }),
                      ],
                    }),
                  (null == (o = m.type) ? void 0 : o.trim()) &&
                    (0, r.jsxs)("div", {
                      children: [
                        (0, r.jsx)("p", {
                          className:
                            "mb-2 font-sans text-[10px]  tracking-[0.14em] text-[#e7e3dd]/90",
                          children: "Year:",
                        }),
                        (0, r.jsx)("p", {
                          className: "font-bueno text-[16px]",
                          children: m.type,
                        }),
                      ],
                    }),
                  (null == (c = m.tools) ? void 0 : c.trim()) &&
                    (0, r.jsxs)("div", {
                      children: [
                        (0, r.jsx)("p", {
                          className:
                            "mb-2 font-sans text-[10px]  tracking-[0.14em] text-[#e7e3dd]/90",
                          children: "Tools:",
                        }),
                        (0, r.jsx)("p", {
                          className:
                            "whitespace-pre-line font-bueno text-[16px] leading-[1.4]",
                          children: m.tools,
                        }),
                      ],
                    }),
                ],
              }),
          ],
        });
      }
      function j() {
        return (0, r.jsxs)("article", {
          className: "pb-16",
          children: [
            (0, r.jsx)("section", {
              className: "relative left-1/2 w-screen -translate-x-1/2",
              children: (0, r.jsxs)("div", {
                className: "relative h-[75svh] min-h-[430px] max-h-[820px]",
                children: [
                  (0, r.jsx)("img", {
                    src: "/rk-about.jpg",
                    alt: "Portrait of Rustam Kerimov",
                    className:
                      "absolute inset-0 h-full w-full object-cover object-center",
                    decoding: "async",
                  }),
                  (0, r.jsxs)("h1", {
                    className:
                      " absolute bottom-[-0.52em] left-[5%] z-10 font-bueno text-2xl font-bold uppercase leading-[0.85] tracking-[-0.045em] text-[#e7e3dd] ",
                    children: [
                      (0, r.jsx)(x, {
                        text: "Behind\nThe Work.",
                        delay: 0.2,
                        stagger: 0.12,
                      }),
                      " ",
                    ],
                  }),
                ],
              }),
            }),
            (0, r.jsxs)("div", {
              className: "pt-[clamp(105px,22vw,150px)]",
              children: [
                (0, r.jsxs)("div", {
                  className:
                    "max-w-[500px] space-y-7  text-[clamp(19px,5vw,24px)] leading-[1.4] text-[#e7e3dd]/90",
                  children: [
                    (0, r.jsx)("p", {
                      children:
                        "A graphic designer exploring visual identities, typography and motion.",
                    }),
                    (0, r.jsx)("p", {
                      className: "text-[#e7e3dd]//90",
                      children:
                        "Creating distinctive visual experiences across branding, editorial design, art direction and animation.",
                    }),
                  ],
                }),
                (0, r.jsx)("p", {
                  className:
                    "mt-12 font-sans text-[11px] uppercase tracking-[0.1em] text-[#e7e3dd]/90",
                  children: "Oslo, Norway / Age: 27",
                }),
              ],
            }),
            (0, r.jsxs)("section", {
              className: "mt-24",
              children: [
                (0, r.jsx)("h2", {
                  className:
                    "mb-12 font-bueno text-lg font-bold  leading-none tracking-[-0.035em]",
                  children: "Services:",
                }),
                (0, r.jsx)("div", {
                  className: "space-y-20",
                  children: m.map((e) =>
                    (0, r.jsxs)(
                      "section",
                      {
                        children: [
                          (0, r.jsx)("h3", {
                            className:
                              "mb-5 font-bueno text-xl font-bold uppercase leading-[1.05] tracking-[-0.025em]",
                            children: e.title,
                          }),
                          (0, r.jsx)("div", {
                            className: "w-full overflow-hidden bg-[#1e211b]",
                            children:
                              "video" === e.type
                                ? (0, r.jsx)("video", {
                                    className:
                                      "pointer-events-none block h-auto w-full",
                                    src: e.src,
                                    autoPlay: !0,
                                    muted: !0,
                                    loop: !0,
                                    playsInline: !0,
                                    preload: "auto",
                                    disablePictureInPicture: !0,
                                    "aria-label": e.title,
                                  })
                                : (0, r.jsx)("img", {
                                    src: e.src,
                                    alt: e.title,
                                    className: "block h-auto w-full",
                                    loading: "lazy",
                                    decoding: "async",
                                  }),
                          }),
                          (0, r.jsx)("p", {
                            className:
                              "mt-6 max-w-[490px] font-bueno text-[clamp(17px,4.5vw,21px)] leading-[1.45] text-[#e7e3dd]/90",
                            children: e.description,
                          }),
                        ],
                      },
                      e.title,
                    ),
                  ),
                }),
              ],
            }),
          ],
        });
      }
      function y(e) {
        var t;
        let { projects: n } = e,
          a = (0, s.usePathname)(),
          [i, o] = (0, l.useState)(() => p(a));
        ((0, l.useEffect)(() => {
          let e = document.documentElement,
            t = document.body,
            n = e.style.overflow,
            r = t.style.overflow;
          return (
            (e.style.overflow = "auto"),
            (t.style.overflow = "auto"),
            () => {
              ((e.style.overflow = n), (t.style.overflow = r));
            }
          );
        }, []),
          (0, l.useEffect)(() => {
            o(p(a));
          }, [a]),
          (0, l.useEffect)(() => {
            let e = () => {
              (o(p(window.location.pathname)), window.scrollTo(0, 0));
            };
            return (
              window.addEventListener("popstate", e),
              () => {
                window.removeEventListener("popstate", e);
              }
            );
          }, []));
        let c = (0, l.useCallback)((e) => {
            let t = p(e);
            (p(window.location.pathname) !== t &&
              window.history.pushState(null, "", t),
              o(t),
              window.scrollTo(0, 0),
              window.dispatchEvent(new PopStateEvent("popstate")));
          }, []),
          u = "/about" === i,
          m = (function (e) {
            let t = e.match(/^\/project\/([^/]+)$/);
            if (!t) return null;
            try {
              return decodeURIComponent(t[1]);
            } catch (e) {
              return null;
            }
          })(i),
          x =
            null === m
              ? null
              : null != (t = n.find((e) => String(e.id) === m))
                ? t
                : null;
        return (0, r.jsxs)(r.Fragment, {
          children: [
            (0, r.jsx)(d.A, { threeReady: !0 }),
            (0, r.jsx)("div", {
              "data-lenis-prevent": !0,
              "data-lenis-prevent-wheel": !0,
              className:
                " relative min-h-svh w-full overflow-x-clip bg-[#0b0c09] text-[#e7e3dd] ",
              children: (0, r.jsxs)("div", {
                className: "w-full px-[5%] ".concat(u ? "pt-0" : "pt-[72px]"),
                children: [
                  (0, r.jsx)(
                    "main",
                    {
                      children:
                        u || null !== m
                          ? u
                            ? (0, r.jsx)(j, {})
                            : x
                              ? (0, r.jsx)(v, { project: x })
                              : (0, r.jsxs)("div", {
                                  className: "py-24",
                                  children: [
                                    (0, r.jsx)("h1", {
                                      className:
                                        "font-bueno text-3xl font-bold uppercase",
                                      children: "Project not found",
                                    }),
                                    (0, r.jsx)("button", {
                                      type: "button",
                                      className: "mt-6 underline",
                                      onClick: () => c("/"),
                                      children: "Back to work",
                                    }),
                                  ],
                                })
                          : (0, r.jsx)(b, { projects: n, navigate: c }),
                    },
                    i,
                  ),
                  (0, r.jsx)(h, {}),
                ],
              }),
            }),
          ],
        });
      }
      function w() {
        return (0, r.jsx)("div", {
          "aria-hidden": "true",
          className: "fixed inset-0 z-[9999] bg-[#0b0c09]",
        });
      }
      let N = i()(
        () => Promise.all([n.e(592), n.e(951), n.e(272)]).then(n.bind(n, 5272)),
        {
          loadableGenerated: { webpack: () => [5272] },
          ssr: !1,
          loading: () => (0, r.jsx)(w, {}),
        },
      );
      function k(e) {
        let { projects: t } = e,
          [n, a] = (0, l.useState)(null);
        return ((0, l.useEffect)(() => {
          let e = window.matchMedia("(max-width: 1023px)"),
            t = () => {
              a(e.matches);
            };
          return (
            t(),
            e.addEventListener("change", t),
            () => {
              e.removeEventListener("change", t);
            }
          );
        }, []),
        null === n)
          ? (0, r.jsx)(w, {})
          : n
            ? (0, r.jsx)(y, { projects: t })
            : (0, r.jsx)(N, { projects: t });
      }
    },
    4760: (e, t, n) => {
      "use strict";
      n.d(t, { m: () => x, A: () => f });
      var r = n(5155),
        a = n(3967),
        i = n(2115),
        l = n(3264),
        s = n(2421);
      let o = (e) => e,
        c = (e) => {
          let t = (0, s.y)(e),
            n = (e) =>
              (function (e, t = o) {
                let n = i.useSyncExternalStore(
                  e.subscribe,
                  () => t(e.getState()),
                  () => t(e.getInitialState()),
                );
                return (i.useDebugValue(n), n);
              })(t, e);
          return (Object.assign(n, t), n);
        },
        d = 0,
        u = ((e) => (e ? c(e) : c))(
          (e) => (
            (l.h_9.onStart = (t, n, r) => {
              e({
                active: !0,
                item: t,
                loaded: n,
                total: r,
                progress: ((n - d) / (r - d)) * 100,
              });
            }),
            (l.h_9.onLoad = () => {
              e({ active: !1 });
            }),
            (l.h_9.onError = (t) => e((e) => ({ errors: [...e.errors, t] }))),
            (l.h_9.onProgress = (t, n, r) => {
              (n === r && (d = r),
                e({
                  active: !0,
                  item: t,
                  loaded: n,
                  total: r,
                  progress: ((n - d) / (r - d)) * 100 || 100,
                }));
            }),
            {
              errors: [],
              active: !1,
              progress: 0,
              item: "",
              loaded: 0,
              total: 0,
            }
          ),
        );
      var m = n(6799);
      let p = [0.76, 0, 0.24, 1];
      function x(e) {
        let { onReady: t } = e,
          n = (0, i.useRef)(0),
          r = (0, i.useRef)(!1),
          l = (0, i.useRef)(null);
        return (
          (0, a.C)(() => {
            !r.current &&
              ((n.current += 1),
              n.current >= 2 &&
                ((r.current = !0),
                (l.current = window.requestAnimationFrame(t))));
          }),
          (0, i.useEffect)(
            () => () => {
              null !== l.current && window.cancelAnimationFrame(l.current);
            },
            [],
          ),
          null
        );
      }
      function f(e) {
        let { threeReady: t, onRevealStart: n } = e,
          { progress: a, active: l, loaded: s, total: o } = u(),
          [c, d] = (0, i.useState)(!1),
          [x, f] = (0, i.useState)(!1),
          h = (0, i.useRef)(null),
          g = (0, i.useRef)(0),
          b = (0, i.useRef)(0),
          v = (0, i.useRef)(!1),
          j = (0, i.useRef)(n),
          y = t && !l && (0 === o || s >= o);
        return ((0, i.useEffect)(() => {
          j.current = n;
        }, [n]),
        (0, i.useEffect)(() => {
          v.current = y;
        }, [y]),
        (0, i.useEffect)(() => {
          Number.isFinite(a) &&
            (b.current = Math.max(b.current, Math.min(100, a)));
        }, [a]),
        (0, i.useEffect)(() => {
          let e = 0,
            t = !1,
            n = performance.now(),
            r = n,
            a = (i) => {
              if (t) return;
              let l = Math.min(Math.max((i - r) / 1e3, 0), 0.05);
              r = i;
              let s = 94 * (1 - Math.exp(-(((i - n) / 1e3) * 2)));
              if (
                ((g.current = Math.min(
                  v.current ? 100 : Math.min(96, Math.max(s, b.current)),
                  g.current + 95 * l,
                )),
                h.current &&
                  (h.current.style.clipPath = "inset(0 ".concat(
                    100 - g.current,
                    "% 0 0)",
                  )),
                v.current && g.current >= 100)
              ) {
                var o;
                ((t = !0), null == (o = j.current) || o.call(j), d(!0));
                return;
              }
              e = window.requestAnimationFrame(a);
            };
          return (
            (e = window.requestAnimationFrame(a)),
            () => {
              window.cancelAnimationFrame(e);
            }
          );
        }, []),
        x)
          ? null
          : (0, r.jsx)(m.P.div, {
              initial: !1,
              animate: { y: c ? "-100%" : "0%" },
              transition: { duration: 0.85, ease: p },
              onAnimationComplete: () => {
                c && f(!0);
              },
              className:
                " fixed inset-0 z-[9999] flex items-center justify-center overflow-hidden bg-[#0e100c] text-[#e7e3dd] ",
              role: "status",
              "aria-label": "Loading portfolio",
              "aria-live": "off",
              children: (0, r.jsxs)("div", {
                className:
                  " relative inline-block select-none font-bueno text-xl font-medium uppercase leading-none tracking-[0.22em] ",
                children: [
                  (0, r.jsx)("span", {
                    className: "text-[#e7e3dd]/20",
                    children: "KERIMOV DESIGNS",
                  }),
                  (0, r.jsx)("span", {
                    ref: h,
                    "aria-hidden": "true",
                    className:
                      " absolute inset-0 whitespace-nowrap text-[#e7e3dd] ",
                    style: { clipPath: "inset(0 100% 0 0)" },
                    children: "KERIMOV DESIGNS",
                  }),
                ],
              }),
            });
      }
    },
    5744: (e, t, n) => {
      "use strict";
      (Object.defineProperty(t, "__esModule", { value: !0 }),
        Object.defineProperty(t, "workAsyncStorage", {
          enumerable: !0,
          get: function () {
            return r.workAsyncStorageInstance;
          },
        }));
      let r = n(7828);
    },
    6645: (e, t, n) => {
      "use strict";
      (Object.defineProperty(t, "__esModule", { value: !0 }),
        Object.defineProperty(t, "default", {
          enumerable: !0,
          get: function () {
            return a;
          },
        }));
      let r = n(8229)._(n(7357));
      function a(e, t) {
        var n;
        let a = {};
        "function" == typeof e && (a.loader = e);
        let i = { ...a, ...t };
        return (0, r.default)({
          ...i,
          modules: null == (n = i.loadableGenerated) ? void 0 : n.modules,
        });
      }
      ("function" == typeof t.default ||
        ("object" == typeof t.default && null !== t.default)) &&
        void 0 === t.default.__esModule &&
        (Object.defineProperty(t.default, "__esModule", { value: !0 }),
        Object.assign(t.default, t),
        (e.exports = t.default));
    },
    7357: (e, t, n) => {
      "use strict";
      (Object.defineProperty(t, "__esModule", { value: !0 }),
        Object.defineProperty(t, "default", {
          enumerable: !0,
          get: function () {
            return o;
          },
        }));
      let r = n(5155),
        a = n(2115),
        i = n(2146);
      function l(e) {
        return { default: e && "default" in e ? e.default : e };
      }
      n(255);
      let s = {
          loader: () => Promise.resolve(l(() => null)),
          loading: null,
          ssr: !0,
        },
        o = function (e) {
          let t = { ...s, ...e },
            n = (0, a.lazy)(() => t.loader().then(l)),
            o = t.loading;
          function c(e) {
            let l = o
                ? (0, r.jsx)(o, { isLoading: !0, pastDelay: !0, error: null })
                : null,
              s = !t.ssr || !!t.loading,
              c = s ? a.Suspense : a.Fragment,
              d = t.ssr
                ? (0, r.jsxs)(r.Fragment, {
                    children: [null, (0, r.jsx)(n, { ...e })],
                  })
                : (0, r.jsx)(i.BailoutToCSR, {
                    reason: "next/dynamic",
                    children: (0, r.jsx)(n, { ...e }),
                  });
            return (0, r.jsx)(c, {
              ...(s ? { fallback: l } : {}),
              children: d,
            });
          }
          return ((c.displayName = "LoadableComponent"), c);
        };
    },
    7828: (e, t, n) => {
      "use strict";
      (Object.defineProperty(t, "__esModule", { value: !0 }),
        Object.defineProperty(t, "workAsyncStorageInstance", {
          enumerable: !0,
          get: function () {
            return r;
          },
        }));
      let r = (0, n(4054).createAsyncLocalStorage)();
    },
    9543: (e, t, n) => {
      (Promise.resolve().then(n.bind(n, 4656)),
        Promise.resolve().then(n.bind(n, 613)));
    },
  },
]);
