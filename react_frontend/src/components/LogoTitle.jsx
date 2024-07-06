import mediTranslateLogo from '../assets/logo.png';

export default function LogoAndName() {
    return(
        <div className="left-0 flex items-center space-x-2 ml-1 mb-4">
            <img src={mediTranslateLogo} alt="meditranslate logo" className= "object-contain mb-8 w-12 h-16"/>
            <h1 className="text-3xl font-roboto-condensed font-bold bg-custom-gradient bg-clip-text text-transparent mb-7 ">
            Meditranslate AI
            </h1>
      </div>
    )
}