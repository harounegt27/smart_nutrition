import { useStore } from '../store/useStore';

const InputForm = () => {
  const { userData, setUserData, fetchResults, isLoading } = useStore();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setUserData({ [name]: type === 'checkbox' ? checked : value });
  };

  return (
    <div className="bg-dark-200 p-6 rounded-2xl border border-dark-300 shadow-lg">
      <h2 className="text-xl font-semibold mb-6 text-white">Vos Informations</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input label="Âge" name="age" type="number" value={userData.age} onChange={handleChange} />
        <Select label="Genre" name="gender" value={userData.gender} onChange={handleChange} options={['Male', 'Female', 'Other']} />
        <Input label="Taille (cm)" name="height_cm" type="number" value={userData.height_cm} onChange={handleChange} />
        <Input label="Poids (kg)" name="weight_kg" type="number" value={userData.weight_kg} onChange={handleChange} />
        <Select label="Activité" name="activity_level" value={userData.activity_level} onChange={handleChange} options={['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active']} />
        <Input label="Sommeil (h)" name="sleep_hours" type="number" step="0.5" value={userData.sleep_hours} onChange={handleChange} />
      </div>

      <div className="mt-6 flex flex-wrap items-center gap-4">
        <CheckBox label="Diabète" name="has_diabetes" checked={userData.has_diabetes} onChange={handleChange} />
        <CheckBox label="Hypertension" name="has_hypertension" checked={userData.has_hypertension} onChange={handleChange} />
        <CheckBox label="Fumeur" name="smoking_habit" checked={userData.smoking_habit === 'Yes'} onChange={(e) => setUserData({ smoking_habit: e.target.checked ? 'Yes' : 'No' })} />
      </div>

      <button 
        onClick={fetchResults}
        disabled={isLoading}
        className="w-full mt-6 py-3 bg-primary hover:bg-primary/90 rounded-xl text-white font-semibold transition-all duration-300 disabled:opacity-50 flex items-center justify-center gap-2"
      >
        {isLoading ? 'Calcul en cours...' : 'Calculer'}
      </button>
    </div>
  );
};

// Composants UI réutilisables
const Input = ({ label, ...props }) => (
  <div>
    <label className="text-xs text-gray-400 mb-1 block">{label}</label>
    <input {...props} className="w-full bg-dark-100 border border-dark-300 rounded-lg p-2.5 text-white focus:border-primary outline-none transition-colors" />
  </div>
);

const Select = ({ label, options, ...props }) => (
  <div>
    <label className="text-xs text-gray-400 mb-1 block">{label}</label>
    <select {...props} className="w-full bg-dark-100 border border-dark-300 rounded-lg p-2.5 text-white focus:border-primary outline-none">
      {options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
    </select>
  </div>
);

const CheckBox = ({ label, ...props }) => (
  <label className="flex items-center gap-2 cursor-pointer text-gray-300 text-sm">
    <input type="checkbox" {...props} className="w-4 h-4 accent-primary bg-dark-100 border-dark-300 rounded" />
    {label}
  </label>
);

export default InputForm;