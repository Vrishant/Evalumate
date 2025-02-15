import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { motion } from 'framer-motion';
import Navbar from '../components/navbar';
import Footer from '../components/footer';
import Particles from '../components/particles';
import GradientText from '../components/gradientText';

const About = () => {
  return (
    <Container fluid className="min-vh-100 d-flex flex-column" style={{ backgroundColor: "#000000", color: "#FFFFFF", fontFamily: "Rasa, sans-serif" }}>
      <Navbar username="JohnDoe" />
      <Row className="flex-grow-1" style={{ position: 'relative' }}>
        <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", zIndex: 0 }}>
          <Particles 
            particleCount={900}
            particleSpread={2}
            speed={0.1}
            particleColors={["#2BC6D1", "#28007B", "#FFFFFF"]}
            moveParticlesOnHover={true}
            particleHoverFactor={1.2}
            alphaParticles={true}
            particleBaseSize={50}
            sizeRandomness={0.5}
            cameraDistance={15}
            disableRotation={false}
          />
        </div>
        
        <Col className="p-4 d-flex flex-column" style={{ position: "relative", zIndex: 1 }}>
          <motion.div 
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            <h1 className="cube-logo" style={{ fontSize: "4rem", fontWeight: "bolder", textShadow: "0px 0px 10px rgba(0, 0,0, 0.5)", textAlign: "center" }}>
              <GradientText
                colors={["#2BC6D1", "#2BC6D1", "#2BC6D1", "#28007B", "#2BC6D1"]}
                animationSpeed={8}
                showBorder={false}
                className="custom-class"
              >
                About <em>Evalumate</em>
              </GradientText>
            </h1>
          </motion.div>

          <Row className="mt-5 justify-content-center">
            <Col md={8}>
              <div style={{ backgroundColor: 'rgba(43, 198, 209, 0.1)', padding: '2rem', borderRadius: '15px', backdropFilter: 'blur(5px)' }}>
                <h2 style={{ color: "#2BC6D1", fontSize: "2rem", fontWeight: "bold" }}>Our Mission</h2>
                <p style={{ fontSize: "1.2rem", lineHeight: "1.8" }}>
                  At <em>Evalumate</em>, we're revolutionizing the way you organize and interact with your notes. Our mission is to provide a seamless, intelligent platform that adapts to your workflow and enhances your productivity.
                </p>

                <h2 style={{ color: "#2BC6D1", fontSize: "2rem", fontWeight: "bold", marginTop: "2rem" }}>Key Features</h2>
                <ul style={{ fontSize: "1.2rem", lineHeight: "1.8", listStyleType: 'none', paddingLeft: 0 }}>
                  <li style={{ marginBottom: '1rem' }}>
                    <span style={{ color: "#2BC6D1", fontWeight: "bold" }}>• Smart Document Processing:</span> Understands and extracts insights from any uploaded document.
                  </li>
                  <li style={{ marginBottom: '1rem' }}>
                    <span style={{ color: "#2BC6D1", fontWeight: "bold" }}>• AI-Powered Summarization:</span> Generates concise yet meaningful summaries for quick comprehension.
                  </li>
                  <li style={{ marginBottom: '1rem' }}>
                    <span style={{ color: "#2BC6D1", fontWeight: "bold" }}>• Context-Aware Q&A:</span> Answers questions strictly based on uploaded content, suggesting related concepts when needed.

                  </li>
                  <li style={{ marginBottom: '1rem' }}>
                    <span style={{ color: "#2BC6D1", fontWeight: "bold" }}>• Intelligent Evaluation:</span> Analyzes structured reports or answer sheets, highlighting key differences from ideal responses.
                  </li>
                </ul>

                <h2 style={{ color: "#2BC6D1", fontSize: "2rem", fontWeight: "bold", marginTop: "2rem" }}>Our Team</h2>
                <p style={{ fontSize: "1.2rem", lineHeight: "1.8" }}>
                  We're a passionate group of developers, designers, and AI enthusiasts dedicated to creating the best note-taking experience possible. Our team combines technical expertise with a deep understanding of user needs to deliver innovative solutions. 🙂
                </p>
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
      <Footer />
    </Container>
  );
};

export default About;
