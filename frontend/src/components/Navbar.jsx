import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <header className="border-b border-slate-200 bg-white/90 backdrop-blur sticky top-0 z-20">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <Link to="/" className="text-lg font-semibold text-slate-900">
          Resume Screening AI
        </Link>

        <nav className="hidden items-center gap-6 text-sm text-slate-600 md:flex">
          <a href="#how-it-works" className="transition hover:text-slate-900">
            How it works
          </a>
          <a href="#features" className="transition hover:text-slate-900">
            Features
          </a>
          <a href="#contact" className="transition hover:text-slate-900">
            Contact
          </a>
        </nav>

        <a
          href="#upload"
          className="rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800"
        >
          Start analysis
        </a>
      </div>
    </header>
  );
}

export default Navbar;
