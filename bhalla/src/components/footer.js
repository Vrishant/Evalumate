import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Envelope, Instagram, Discord } from 'react-bootstrap-icons'; // Import specific icons

const Footer = () => {
  return (
    <footer
      className="text-light py-4"
      style={{
        background: 'linear-gradient(135deg, rgb(0, 0, 0), rgb(36, 36, 36))', // Gradient background
      }}
    >
      <div className="container">
        <div className="row">
          {/* About Section */}
          <div className="col-md-4">
            <h5>About <span style={{ fontStyle: 'italic', fontWeight: 'bold', color: 'rgb(27, 166, 205)' }}>Evalumate</span></h5>
            <p>
              <span style={{ fontStyle: 'italic', fontWeight: 'bold' }}>GCUBE</span> is your ultimate platform for game development and creativity.  
              <strong> Get. Game. Going.</strong>
            </p>
          </div>

          {/* Quick Links */}
          <div className="col-md-4">
            <h5 className="text-info">Quick Links</h5>
            <ul className="list-unstyled">
              <li><a href="/" className="text-light text-decoration-none">Home</a></li>
              <li><a href="/about" className="text-light text-decoration-none">About</a></li>
            </ul>
          </div>

          {/* Social Media */}
          <div className="col-md-4 text-info">
            <h5>Follow Us</h5>
            <div>
              <a href="/" className="text-light me-3">
                <Envelope size={24} />
              </a>
              <a href="https://www.instagram.com/vrishant.bhalla/" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-light me-3">
                <Instagram size={24} />
              </a>
              <a href="#" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-light me-3">
                <Discord size={24} />
              </a>
            </div>
          </div>
        </div>

        <hr className="border-light" />

        {/* Copyright Section */}
        <div className="text-center">
          <p className="mb-0">&copy; 2025 Evalumate. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
