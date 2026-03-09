import { useStore } from '../store/useStore';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';
import { Flame, Apple, Wheat, Droplet } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ResultDisplay = () => {
  const { results } = useStore();
  if (!results) return null;

  const data = [
    { name: 'Protéines', value: results.recommended_protein, color: '#f87171' },
    { name: 'Glucides', value: results.recommended_carbs, color: '#60a5fa' },
    { name: 'Lipides', value: results.recommended_fats, color: '#fbbf24' },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Cartes Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard icon={<Flame className="text-orange-400" />} label="Calories" value={`${results.recommended_calories} kcal`} />
        <StatCard icon={<Apple className="text-red-400" />} label="Protéines" value={`${results.recommended_protein}g`} />
        <StatCard icon={<Wheat className="text-blue-400" />} label="Glucides" value={`${results.recommended_carbs}g`} />
        <StatCard icon={<Droplet className="text-yellow-400" />} label="Lipides" value={`${results.recommended_fats}g`} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Graphique */}
        <div className="bg-dark-100 p-6 rounded-2xl border border-dark-200 shadow-lg">
          <h3 className="text-lg font-semibold text-white mb-4">Répartition Macros</h3>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data} cx="50%" cy="50%" innerRadius={50} outerRadius={70} paddingAngle={5} dataKey="value">
                  {data.map((entry, index) => <Cell key={index} fill={entry.color} />)}
                </Pie>
                <Legend wrapperStyle={{ color: '#fff' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* BMI */}
        <div className="bg-dark-100 p-6 rounded-2xl border border-dark-200 shadow-lg flex flex-col justify-center items-center">
           <div className={`text-6xl font-bold mb-2 ${results.bmi_category === 'Normal' ? 'text-primary' : 'text-yellow-400'}`}>
             {results.bmi}
           </div>
           <div className="text-gray-400 text-sm mb-4">Indice de Masse Corporelle</div>
           <div className={`px-4 py-1 rounded-full text-sm font-semibold ${results.bmi_category === 'Normal' ? 'bg-primary/20 text-primary' : 'bg-yellow-400/20 text-yellow-400'}`}>
             {results.bmi_category}
           </div>
        </div>
      </div>

      {/* Conseils IA AMÉLIORÉS */}
      <div className="bg-dark-100 p-6 rounded-2xl border border-dark-200 shadow-lg">
        <h3 className="text-xl font-bold text-primary mb-4 flex items-center gap-2">
          🤖 Plan Alimentaire & Conseils
        </h3>
        
        <div className="prose prose-invert max-w-none 
          prose-headings:text-primary prose-headings:font-bold 
          prose-h2:text-lg prose-h2:mt-6 prose-h2:mb-2 prose-h2:border-b prose-h2:border-dark-200 prose-h2:pb-2
          prose-p:text-gray-300 prose-p:leading-relaxed
          prose-ul:text-gray-300 prose-li:marker:text-primary
        ">
          <ReactMarkdown
            components={{
              h2: ({ node, ...props }) => <h2 className="text-white font-bold text-lg mt-4 mb-2" {...props} />,
              h3: ({ node, ...props }) => <h3 className="text-primary font-semibold text-md mt-3 mb-1" {...props} />,
              ul: ({ node, ...props }) => <ul className="list-disc list-inside space-y-1 text-gray-300 mb-4" {...props} />,
              p: ({ node, ...props }) => <p className="text-gray-300 mb-2" {...props} />
            }}
          >
            {results.ai_advice}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value }) => (
  <div className="bg-dark-100 p-4 rounded-xl border border-dark-200 flex items-center gap-4 shadow-sm">
    <div className="p-3 bg-dark rounded-lg border border-dark-200">{icon}</div>
    <div>
      <p className="text-xs text-gray-400">{label}</p>
      <p className="text-lg font-bold text-white">{value}</p>
    </div>
  </div>
);

export default ResultDisplay;