import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import Configuration from './components/Configuration';
import Mentions from './components/Mentions';
import Logs from './components/Logs';
import { ApiProvider } from './context/ApiContext';

function App() {
  return (
    <ApiProvider>
      <Router>
        <div className="App">
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/config" element={<Configuration />} />
              <Route path="/mentions" element={<Mentions />} />
              <Route path="/logs" element={<Logs />} />
            </Routes>
          </Layout>
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </div>
      </Router>
    </ApiProvider>
  );
}

export default App;
