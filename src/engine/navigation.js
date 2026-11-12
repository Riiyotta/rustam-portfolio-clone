/**
 * Stand-in for next/navigation. The original app drives its own URL state with
 * history.pushState + popstate; Next's usePathname follows pushState, so we
 * mirror that by notifying subscribers whenever history changes.
 */
import { useSyncExternalStore } from 'react';

const EVENT = 'app:locationchange';
const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

for (const method of ['pushState', 'replaceState']) {
  const original = history[method];
  history[method] = function (...args) {
    const result = original.apply(this, args);
    window.dispatchEvent(new Event(EVENT));
    return result;
  };
}
window.addEventListener('popstate', emit);
window.addEventListener(EVENT, emit);

const subscribe = (cb) => {
  listeners.add(cb);
  return () => listeners.delete(cb);
};
const getPath = () => window.location.pathname;

export function usePathname() {
  return useSyncExternalStore(subscribe, getPath, getPath);
}

const router = {
  push: (href) => history.pushState(null, '', href),
  replace: (href) => history.replaceState(null, '', href),
  back: () => history.back(),
  forward: () => history.forward(),
  refresh: () => {},
  prefetch: () => {},
};

export function useRouter() {
  return router;
}
