import React from 'react';

const LoadingPage = () => {
  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#f5f5f5',
    }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <div style={{
          width: '50px',
          height: '50px',
          border: '4px solid #333',
          borderTop: '4px solid #f00',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
        }} />
        <h1 style={{ marginTop: '20px' }}>Loading...</h1>
      </div>
    </div>
  );
}

export default LoadingPage;