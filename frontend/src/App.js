import React, { useState } from 'react';
import './App.css';

function App() {
  const [display, setDisplay] = useState('');
  const [error, setError] = useState('');

  const appendToDisplay = (value) => {
    setDisplay(display + value);
    setError('');
  };

  const clearDisplay = () => {
    setDisplay('');
    setError('');
  };

  const calculate = async () => {
    if (!display) {
      setError('Введите выражение');
      return;
    }
    try {
      const apiUrl = 'http://dispatcher:8000/calculate';
      console.log('Sending request to:', apiUrl, 'with body:', { expression: display });
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression: display })
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
      }
      const data = await response.json();
      console.log('Response:', data);
      if (data.result !== undefined) {
        setDisplay(data.result.toString());
        setError('');
      } else {
        setDisplay('');
        setError('Неверный формат ответа от сервера');
      }
    } catch (error) {
      console.error('Calculation error:', error.message);
      setDisplay('');
      setError(`Ошибка: ${error.message}`);
    }
  };

  return (
    <div className="calculator">
      {error && <div className="error">{error}</div>}
      <input type="text" value={display} readOnly />
      <div className="buttons">
        <button onClick={clearDisplay}>C</button>
        <button onClick={() => appendToDisplay('7')}>7</button>
        <button onClick={() => appendToDisplay('8')}>8</button>
        <button onClick={() => appendToDisplay('9')}>9</button>
        <button onClick={() => appendToDisplay('/')}>/</button>
        <button onClick={() => appendToDisplay('4')}>4</button>
        <button onClick={() => appendToDisplay('5')}>5</button>
        <button onClick={() => appendToDisplay('6')}>6</button>
        <button onClick={() => appendToDisplay('*')}>*</button>
        <button onClick={() => appendToDisplay('1')}>1</button>
        <button onClick={() => appendToDisplay('2')}>2</button>
        <button onClick={() => appendToDisplay('3')}>3</button>
        <button onClick={() => appendToDisplay('-')}>-</button>
        <button onClick={() => appendToDisplay('0')}>0</button>
        <button onClick={() => appendToDisplay('.')}>.</button>
        <button onClick={calculate}>=</button>
        <button onClick={() => appendToDisplay('+')}>+</button>
      </div>
    </div>
  );
}

export default App;