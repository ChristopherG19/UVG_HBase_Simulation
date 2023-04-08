import React, { useState } from 'react';
import './styles/Terminal.css';

const TerminalPage = () => {
  const [input, setInput] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(input);
    setMessage(input)
    setInput('');
    setError('Error: Comando no encontrado');
  };

  return (
    <div className="container">
      <div className="terminal">
        <div className="terminal-header">
          <span>Terminal</span>
        </div>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="terminal-input"
            placeholder="Ingrese un comando..."
          />
          <button type="submit" className="terminal-button">
            Enviar
          </button>
        </form>
        <div className="terminal-error">{error}</div>
        <div className="terminal-output">{message}</div>
      </div>
    </div>
  );
};

export default TerminalPage;
