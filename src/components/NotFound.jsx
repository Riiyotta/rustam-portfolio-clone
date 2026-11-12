import { require } from '../engine/runtime';
import '../engine/chunks/notfound.js';

const FloatingDigits = require(9812).default; // original three.js "404" scene

export default function NotFound() {
  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-dark px-6 text-color">
      <FloatingDigits />
      <section className=" absolute left-10 bottom-6 z-10 max-w-3xl text-left">
        <h1 className="sr-only">404</h1>
        <h2 className="mt-4 text-3xl font-semibold md:text-5xl">This page got lost.</h2>
        <p className="mx-auto mt-3 max-w-xl text-lg text-white/60 md:text-xl">
          The page you’re looking for doesn’t exist, but my portfolio is still right where it should be.
        </p>
        <a
          href="/"
          className="group mt-2 inline-flex items-center gap-4 text-lg font-black uppercase tracking-[-0.02em] text-white transition-opacity duration-300 hover:opacity-70"
        >
          <span className="block h-20 w-20 overflow-visible" aria-hidden="true">
            <svg
              viewBox="0 0 48 24"
              className="h-full w-full overflow-visible fill-none stroke-current"
              strokeWidth="1.5"
              strokeLinecap="square"
              strokeLinejoin="miter"
            >
              <path d="M44 12H14" />
              <path
                d="M14 12L24 4"
                className="origin-[14px_12px] scale-0 transition-transform duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] group-hover:scale-100"
              />
            </svg>
          </span>
          <span>Back to portfolio</span>
        </a>
      </section>
    </main>
  );
}
