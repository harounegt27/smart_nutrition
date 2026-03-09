import { create } from 'zustand';
import axios from 'axios';

export const useStore = create((set) => ({
  // 1. Données par défaut du formulaire
  userData: {
    age: 25,
    gender: 'Male',
    height_cm: 175,
    weight_kg: 70,
    activity_level: 'Moderate',
    dietary_habits: 'Regular',
    sleep_hours: 7,
    alcohol_consumption: 'No',
    smoking_habit: 'No',
    has_diabetes: false,
    has_hypertension: false,
    allergies: '',
  },
  
  // 2. États de l'application
  results: null, // Stockera la réponse de l'API
  isLoading: false,
  error: null,
  history: [],
  // 3. Actions
  // Mettre à jour les champs du formulaire
  setUserData: (data) => set((state) => ({ 
    userData: { ...state.userData, ...data } 
  })),
  
  // Appeler l'API FastAPI
  fetchResults: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', useStore.getState().userData);
      const newResult = response.data;
      
      set((state) => ({ 
        results: newResult, 
        isLoading: false,
        history: [newResult, ...state.history] 
      }));
    } catch (error) {
      set({ error: "Erreur de connexion à l'API", isLoading: false });
      console.error(error);
    }
  }
}));