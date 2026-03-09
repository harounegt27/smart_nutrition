import { useStore } from '../store/useStore';
import { History, Eye } from 'lucide-react';

const HistoryPage = () => {
  const { history } = useStore();

  return (
    <div className="p-4 md:p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <History className="text-primary" /> Historique
        </h1>
        <p className="text-gray-400 mt-1">Retrouvez vos précédentes analyses de cette session.</p>
      </header>

      {history.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <p>Aucune prédiction effectuée pour le moment.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {history.map((item, index) => (
            <div key={index} className="bg-dark-100 border border-dark-200 rounded-xl p-6 hover:border-primary transition-colors">
              <div className="flex justify-between items-center mb-4">
                <span className="text-sm text-gray-400">Prédiction #{history.length - index}</span>
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-primary/20 text-primary">
                  {item.bmi_category}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-4 text-white">
                <div>
                  <span className="text-xs text-gray-400">Calories</span>
                  <p className="text-xl font-bold">{item.recommended_calories} <span className="text-sm font-normal">kcal</span></p>
                </div>
                <div>
                  <span className="text-xs text-gray-400">IMC</span>
                  <p className="text-xl font-bold">{item.bmi}</p>
                </div>
              </div>
              {/* Bouton voir détails (optionnel, ici juste visuel) */}
              <button className="mt-4 w-full flex items-center justify-center gap-2 text-sm text-gray-400 hover:text-primary py-2 border-t border-dark-200 pt-4">
                <Eye size={16} /> Voir les détails
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HistoryPage;