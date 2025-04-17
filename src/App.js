// App.js
import './App.css';
import Navbar from "./components/Navbar";
import GlassyForm from "./components/GlassyForm";
import ResultsPage from './components/ResultsPage'; // Make sure this path is correct
import ConfirmationPage from "./components/ConfirmationPage";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Use Routes instead of Switch

function App() {
    return (
        <Router>
            <div className="App">
                <Navbar />
                <Routes>
                    <Route path="/" element={<GlassyForm />} />
                    <Route path="/results" element={<ResultsPage />} />
                    <Route path="/confirmation" element={<ConfirmationPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
