import React from 'react';
import { Link } from 'react-router-dom';
import './styles/Menu.css';

const Menu = () => {
  return (
    <div className="menu-container">
      <div className="menu-content">
        <div className="menu-header">
          <h2 className="menu-title">¿Cuál es el propósito?</h2>
        </div>
        <div className="menu-links">
          <Link className="menu-link data" to="/data">
            <button className="menu-button">
              <div className="menu-button-content">
                <span className="menu-link-text">Visualizar data</span>
              </div>
            </button>
          </Link>
          <Link className="menu-link terminal" to="/terminal">
            <button className="menu-button">
              <div className="menu-button-content">
                <span className="menu-link-text">Terminal</span>
              </div>
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Menu;