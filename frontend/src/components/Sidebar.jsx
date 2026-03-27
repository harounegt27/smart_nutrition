import { Home, History, Settings ,Calculator} from 'lucide-react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <aside className="w-64 min-h-screen bg-dark-100 border-r border-dark-200 p-4 hidden md:flex flex-col">
      {/* Header avec Logo */}
      <div className="flex items-center justify-between mb-10 p-2">
        <div className="flex items-center gap-2">
          
        </div>
      </div>
      
      <nav className="space-y-2 flex-grow">
        <NavItem to="/" icon={<Home size={20} />} label="Accueil" />
        <NavItem to="/predict" icon={<Calculator size={20} />} label="Prédiction" end />
        <NavItem to="/history" icon={<History size={20} />} label="Historique" />
      </nav>

      <div className="mt-auto pt-4 border-t border-dark-200">
        <NavItem to="#" icon={<Settings size={20} />} label="Paramètres" />
      </div>
    </aside>
  );
};

const NavItem = ({ to, icon, label }) => (
  <NavLink 
    to={to}
    className={({ isActive }) => `flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all duration-300 
    ${isActive ? 'bg-primary text-dark font-semibold shadow-lg shadow-primary/20' : 'text-gray-400 hover:bg-dark-200 hover:text-white'}`}
  >
    {icon}
    <span>{label}</span>
  </NavLink>
);

export default Sidebar;