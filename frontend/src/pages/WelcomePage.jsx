import { useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight } from 'lucide-react';
import smartLogo from '../assets/Smart Nutrition Logo.png';

const WelcomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 text-center bg-dark">
      <div className="max-w-2xl space-y-8">
        
       
        <div className="w-40 h-40 p-5 bg-primary/20 rounded-full mx-auto animate-bounce flex items-center justify-center">
          <img 
            src={smartLogo} 
            alt="Logo" 
            className="w-full h-full object-contain" 
          />
        </div>

        <h1 className="text-5xl font-bold text-white leading-tight">
          Bienvenue sur <span className="text-primary">Smart Nutrition</span>
        </h1>
        
        <p className="text-xl text-gray-300">
          Transformez votre santé avec l'intelligence artificielle. Obtenez des recommandations nutritionnelles personnalisées et un plan alimentaire adapté à votre mode de vie.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left my-8">
          <FeatureCard title="Analyse IA" description="Prédictions basées sur vos données de santé." />
          <FeatureCard title="Plans Alimentaires" description="Menus détaillés générés automatiquement." />
          <FeatureCard title="Suivi & Conseils" description="Recommandations sportives et hygiène de vie." />
        </div>

        <button 
        onClick={() => navigate('/predict')}
        // Remarquez : suppression de bg-primary, ajout de btn-gradient-animated et text-white
        className="group px-8 py-4 text-white font-bold rounded-xl text-lg transition-all duration-300 flex items-center gap-2 mx-auto btn-gradient-animated shadow-lg hover:scale-105"
        >
        Commencer l'analyse
        <ArrowRight className="group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
};

const FeatureCard = ({ title, description }) => (
  <div className="bg-dark-100 p-6 rounded-xl border border-dark-200 hover:border-primary transition-colors">
    <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
    <p className="text-sm text-gray-400">{description}</p>
  </div>
);

export default WelcomePage;