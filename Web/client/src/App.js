import './App.css';
import React from 'react';
import {Routes, Route, Link} from 'react-router-dom';
import ParamsForm from "./components/ParamsForm";
import About from "./components/About"
import Footer from "./components/Footer";
import Waiting from './components/Waiting';
// import Intro3 from './components/Intro3';



function App() {
  const handleRedirect = () => {
    window.location.replace('https://github.com/tahiri-lab/iPhyloGeo.js')
  };
  return (
    <div className= ".page-body">
      <nav className="navbar navbar-expand-lg navbar-light bg-light nav-pills justify-content-end">
        <Link to="/" className="navbar-brand">HomePage</Link>
        <Link to="/about" className="nav-item navbar-brand">About</Link>
        <botton onClick={handleRedirect} className="nav-item navbar-brand">Github</botton>
      </nav>
      <Routes>
        <Route path="/" element={<ParamsForm />}></Route>
        <Route path="/about" element={<About />}></Route>
        <Route path="/aPhyloGeo" element={<Waiting />}></Route>
      </Routes>

      <br/>
      <br/>
      <Footer />
      
    </div>
  ) 
}

export default App;