import mediTranslateLogo from '../assets/logo.png';
// import LogoTitle from './LogoTitle';

export default function Header() {

  return (
    <header className="relative flex items-center justify-center space-x-4 mt-5 mb-8 ml-5 mr-5">
        <h1 className="text-5xl md:text-6xl mt-12 font-roboto-condensed font-bold bg-custom-gradient bg-clip-text text-transparent "> 
          Translate medicine leaflets
        </h1>
  </header>
  );
}