import React from 'react';
import './Navbar.css';

function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <h1>GrundbuchAI</h1>
                <ul className="navbar-links">
                    <a href="#home" className="nav-item">Home</a>
                    <a href="#services" className="nav-item">Services</a>
                    <a href="#hilfe" className="nav-item">Support</a>

                </ul>
            </div>
        </nav>
    );
}

export default Navbar;
