import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [ id, setId ] = useState('');
  const [ newId, setNewId ] = useState('');
  const [ currentBalance, setCurrentBalance ] = useState('');
  const [ transactions, setTransactions ] = useState([]);


  // useEffect(() => {
  //   axios.get('localhost:4006/mine')
  //     .then(res => {
  //       console.log(res.data)
  //       setCurrentBalance(res.data)
  //     })
  //     .catch(err => {
  //       console.log(err)
  //     })
  // },[])

  useEffect(() => {
    axios.get('localhost:4006/chain')
      .then(res => {
        setTransactions(res.data)
      })
      .catch(err => {
        console.log(err)
      })
  })

  changeId = () => {

  }

  return (
    <div className="App">
      <h1 style={{textAlign: "center"}}>Wallet</h1>
      <input placeholder="Enter id" onChange={(e) => e.target.value} />
      <button onClick={() => enterId()}>Enter id</button>
      <h4 style={{textAlign: "center"}}>Balance: {currentBalance}</h4>
    </div>
  );
}

export default App;
