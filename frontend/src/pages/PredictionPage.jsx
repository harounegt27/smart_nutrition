import InputForm from '../components/InputForme';
import ResultDisplay from '../components/ResultDisplay';
import { useStore } from '../store/useStore';

const PredictionPage = () => {
  const { results } = useStore();

  return (
    <div className="p-4 md:p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white">Tableau de Bord</h1>
        <p className="text-gray-400 mt-1">Entrez vos données pour obtenir vos recommandations.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <InputForm />
        </div>
        <div className="lg:col-span-2">
          {results ? <ResultDisplay /> : <EmptyState />}
        </div>
      </div>
    </div>
  );
};

const EmptyState = () => (
  <div className="h-full flex items-center justify-center border border-dashed border-dark-200 rounded-2xl text-gray-500 min-h-[400px] bg-dark-100/50">
    <div className="text-center p-4">
      <p className="font-semibold text-xl">En attente de données</p>
      <p className="text-sm mt-2">Remplissez le formulaire et cliquez sur 'Calculer'.</p>
    </div>
  </div>
);

export default PredictionPage;