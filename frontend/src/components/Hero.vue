<template>
    <main class="container">
      <div class="card-grid">
        <div class="card">
          <div class="card-icon">
            <i class="fas fa-gamepad"></i>
          </div>
          <div class="card-content">
            <h2>Track Games</h2>
            <p>Keep track of your gaming collection and progress in one place.</p>
            <button class="card-button">Learn More</button>
          </div>
        </div>
        
        <div class="card">
          <div class="card-icon">
            <i class="fas fa-trophy"></i>
          </div>
          <div class="card-content">
            <h2>Achievements</h2>
            <p>Track your achievements and compare with other players.</p>
            <button class="card-button">Learn More</button>
          </div>
        </div>
        
        <div class="card">
          <div class="card-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="card-content">
            <h2>Community</h2>
            <p>Connect with other gamers and share your experiences.</p>
            <button class="card-button">Learn More</button>
          </div>
        </div>
      </div>
    </main>
  </template>
  
  <style scoped>
  .container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .card-grid {
    display: flex;
    gap: 2rem;
    justify-content: space-between;
  }
  
  .card {
    flex: 1;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: transform 0.3s ease;
  }
  
  .card:hover {
    transform: translateY(-5px);
  }
  
  .card-icon {
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8fafc;
    color: #3b82f6;
    font-size: 4rem;
    transition: all 0.3s ease;
  }
  
  .card:hover .card-icon {
    color: #2563eb;
    transform: scale(1.1);
  }
  
  .card-content {
    padding: 1.5rem;
  }
  
  .card-content h2 {
    margin-bottom: 1rem;
    color: #333;
    font-size: 1.25rem;
  }
  
  .card-content p {
    color: #666;
    margin-bottom: 1.5rem;
  }
  
  .card-button {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.2s;
  }
  
  .card-button:hover {
    background: #2563eb;
  }
  
  @media (max-width: 768px) {
    .card-grid {
      flex-direction: column;
    }
    
    .card {
      width: 100%;
    }
  }
  </style>