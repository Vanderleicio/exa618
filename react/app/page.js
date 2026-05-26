"use client"; 

import Image from 'next/image'
import React from 'react';
import { useState, useEffect } from 'react';

function MessageRow({ message }) {
  const msg = message[0]
  const author = message[1]
  const date = message[2]
  return (
    <tr>
      <td style={{ padding: '12px', borderBottom: '1px solid #eee', color: '#555' }}>{author}</td>
      <td style={{ padding: '12px', borderBottom: '1px solid #eee', color: '#555' }}>{msg}</td>
      <td style={{ padding: '12px', borderBottom: '1px solid #eee', color: '#555' }}>{date}</td>
    </tr>
  );
}

function SearchBar({filterText, onFilterTextChange}) {
  return (
    <form>
      <input 
        type="text" 
        value={filterText} 
        placeholder="Search..." 
        onChange={(e) => onFilterTextChange(e.target.value)}
        style={{ width: '100%', padding: '12px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box', fontSize: '16px' }}
      />
    </form>
  );
}

function MessageTable({ messages, filterText}) {
  const rows = [];
  let lastCategory = null;
  messages.forEach((msg, index) => {
    let body = msg[1] !== null && msg[1] !== undefined ? String(msg[0]) : "";
    let autor = msg[0] !== null && msg[0] !== undefined ? String(msg[1]) : "";
    if ((body.toLowerCase().indexOf(filterText.toLowerCase()) === -1) & (autor.toLowerCase().indexOf(filterText.toLowerCase()) === -1) ) {
      return;
    }
    rows.push(
      <MessageRow
        message={msg} 
        key = {index}/>
    );
  });

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
      <thead>
        <tr>
          <th style={{ textAlign: 'left', padding: '12px', borderBottom: '2px solid #ddd', backgroundColor: '#fafafa', color: '#333' }}>Autor</th>
          <th style={{ textAlign: 'left', padding: '12px', borderBottom: '2px solid #ddd', backgroundColor: '#fafafa', color: '#333' }}>Mensagem</th>
          <th style={{ textAlign: 'left', padding: '12px', borderBottom: '2px solid #ddd', backgroundColor: '#fafafa', color: '#333' }}>Data</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}

function FilterableMessageTable ({ messages }){
  const [filterText, setFilterText] = useState('');

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', backgroundColor: 'white', padding: '30px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
      <SearchBar filterText={filterText} 
      onFilterTextChange={setFilterText}/>
      <MessageTable messages={messages} filterText={filterText}/>
    </div>
  ); 
}

export default function Home() {
    
  const [blogMessages, setBlogMessages] = useState([]);
  
  useEffect(() => {
    fetch('https://script.google.com/macros/s/AKfycbzBn3sALe1rYjz7Ze-Ik7q9TEVP0I2V3XX7GNcecWP8NvCzGt4yO_RT1OlQp09TE9cU/exec')
      .then(response => response.json())
      .then(data => {
        console.log(data)
          setBlogMessages(data);
      });
  }, []);
  
    return (
      <main style={{ padding: '40px 20px', fontFamily: 'sans-serif', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
        <FilterableMessageTable messages={blogMessages} />
      </main>
    )
}