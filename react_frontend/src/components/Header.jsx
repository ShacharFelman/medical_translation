import mediTranslateLogo from '../assets/logo.png';
// import LogoTitle from './LogoTitle';

export default function Header() {

  return (
    <header className="relative flex items-center justify-center space-x-4 mt-3 mb-2 ml-5 mr-5">
        <h1 className="text-5xl md:text-6xl mt-3 font-roboto-condensed font-bold bg-custom-gradient bg-clip-text text-transparent "> 
          Translate medicine leaflets
        </h1>
  </header>
  );
}