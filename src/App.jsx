import { require } from './engine/runtime';
import './engine/chunks/layout.js';
import './engine/chunks/924.js';
import './engine/chunks/272.js';
import projects from './data/projects.json';
import NotFound from './components/NotFound.jsx';

// Client components from the original app, resolved by their webpack ids.
const PageTransitionRoot = require(7689).default; // ClientPageTransitionWrapper + preloader canvas
const { HeroIntroProvider } = require(6411);
const { ProjectNavProvider } = require(5411);
const Navbar = require(5883).default;
const { Toaster } = require(3568);
const SmoothScroll = require(613).default; // Lenis provider
const Home = require(4656).default; // gallery (desktop WebGL) / list (mobile)

const toastOptions = {
  style: {
    background: '#ecebeb',
    color: '#1c1a17',
    border: '1px solid #ecebeb',
    fontFamily: 'Satoshi, sans-serif',
  },
  success: { iconTheme: { primary: '#4ade80', secondary: '#1c1a17' } },
  error: { iconTheme: { primary: '#f87171', secondary: '#1c1a17' } },
};

// Routes the original serves with 200: "/", "/about", "/project/:id". Anything else is its 404 page.
const path = window.location.pathname.replace(/\/+$/, '') || '/';
const isKnownRoute = path === '/' || path === '/about' || /^\/project\/[^/]+$/.test(path);

export default function App() {
  return (
    <>
      <PageTransitionRoot>
        <HeroIntroProvider>
          <ProjectNavProvider>
            <Navbar />
            {isKnownRoute ? (
              <SmoothScroll>
                <main className="relative min-h-screen w-full bg-dark text-color">
                  <Home projects={projects} />
                </main>
              </SmoothScroll>
            ) : (
              <NotFound />
            )}
          </ProjectNavProvider>
        </HeroIntroProvider>
      </PageTransitionRoot>
      <Toaster position="top-center" toastOptions={toastOptions} />
    </>
  );
}
