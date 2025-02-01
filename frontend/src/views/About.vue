<template>
    <div class="about-container">
      <h1 class="about-title">About GameTracker</h1>
  
      <div class="card-grid">
        <div class="card">
          <div class="card-icon">
            <i class="fas fa-bullseye"></i>
          </div>
          <div class="card-content">
            <h2>Our Mission</h2>
            <p>GameTracker aims to help gamers track their progress, connect with others, and discover new gaming experiences.</p>
          </div>
        </div>
  
        <div class="card">
          <div class="card-icon">
            <i class="fas fa-history"></i>
          </div>
          <div class="card-content">
            <h2>Our Story</h2>
            <p>Started in 2024, GameTracker was born from a passion for gaming and a desire to build a better gaming community.</p>
          </div>
        </div>
  
        <div class="card">
          <div class="card-icon">
            <i class="fas fa-heart"></i>
          </div>
          <div class="card-content">
            <h2>Our Values</h2>
            <p>We believe in creating an inclusive, supportive environment where gamers can share their passion and achievements.</p>
          </div>
        </div>
      </div>
  
      <div class="team-section">
        <h2>Meet Our Team</h2>
        <div class="team-grid">
          <div class="team-member">
            <div class="member-icon">
              <i class="fas fa-user"></i>
            </div>
            <h3>Arsam Ezzati</h3>
            <p>Founder & Developer</p>
          </div>
  
          <div class="team-member">
            <div class="member-icon">
              <i class="fas fa-user"></i>
            </div>
            <h3>Jim Barton</h3>
            <p>Lead Designer</p>
          </div>
  
          <div class="team-member">
            <div class="member-icon">
              <i class="fas fa-user"></i>
            </div>
            <h3>Mike Johnson</h3>
            <p>Community Manager</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .about-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .about-title {
    font-size: 2.5rem;
    color: #333;
    margin-bottom: 2rem;
    text-align: center;
  }
  
  .card-grid {
    display: flex;
    gap: 2rem;
    margin-bottom: 4rem;
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
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8fafc;
    color: #3b82f6;
    font-size: 3rem;
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
    color: #333;
    font-size: 1.25rem;
    margin-bottom: 1rem;
  }
  
  .card-content p {
    color: #666;
  }
  
  .team-section {
    text-align: center;
    margin-top: 4rem;
  }
  
  .team-section h2 {
    font-size: 2rem;
    color: #333;
    margin-bottom: 2rem;
  }
  
  .team-grid {
    display: flex;
    gap: 2rem;
    justify-content: center;
  }
  
  .team-member {
    flex: 1;
    max-width: 300px;
    text-align: center;
  }
  
  .member-icon {
    width: 100px;
    height: 100px;
    margin: 0 auto 1rem;
    background: #f8fafc;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3b82f6;
    font-size: 2.5rem;
    transition: all 0.3s ease;
  }
  
  .team-member:hover .member-icon {
    background: #3b82f6;
    color: white;
    transform: scale(1.1);
  }
  
  .team-member h3 {
    color: #333;
    margin-bottom: 0.5rem;
  }
  
  .team-member p {
    color: #666;
  }
  
  @media (max-width: 768px) {
    .card-grid, .team-grid {
      flex-direction: column;
    }
  
    .team-member {
      max-width: 100%;
    }
  }
  </style>