import React, { useState, useRef, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Row, Col, Form, InputGroup, Button } from "react-bootstrap";
import { Send } from "react-bootstrap-icons";
import { motion } from "framer-motion";
import Orb from "../components/orb.js";

function App() {
  const [files, setFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatRef = useRef(null);

  const handleFileUpload = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setFiles([...files, ...uploadedFiles]);
  };

  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages([...messages, { sender: "User", text: input, timestamp: new Date().toLocaleTimeString() }]);
      setInput("");
      setTimeout(() => {
        setMessages((prev) => [...prev, { sender: "Bot", text: "This is a bot response.", timestamp: new Date().toLocaleTimeString() }]);
      }, 1000);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Container fluid className="vh-100 d-flex flex-column" style={{ backgroundColor: "#000000", color: "#FFFFFF", fontFamily: "Oswald, sans-serif" }}>
      {/* <div style={{ width: "100%", height: "600px", position: "relative" }}>
        <Orb hoverIntensity={0.5} rotateOnHover={true} hue={0} forceHoverState={false} />
      </div> */}
      <Row className="flex-grow-1">
        <Col md={3} className="vh-100 p-3 border-end d-flex flex-column animate__animated animate__fadeInLeft" style={{ backgroundColor: "#1A1A1A", color: "#FFFFFF",
        //  borderRadius: "20px 0 0 20px", 
         fontFamily: "Zen Dots, sans-serif", 
          // backdropFilter: 'blur(10px)' 
          }}>
          <h4 style={{ color: "#2BC6D1", fontFamily: "Zen Dots, sans-serif",fontWeight: 'Bold' }}><em>Notebook</em></h4>
          <hr style={{ borderColor: "#2BC6D1" }} />
          <Form.Group>
            <Form.Label style={{ color: "#2BC6D1" }}>Upload Documents</Form.Label>
            <Form.Control type="file" multiple onChange={handleFileUpload} style={{ backgroundColor: "#000000", color: "#FFFFFF", borderColor: "#2BC6D1", borderRadius: "10px" }} />
          </Form.Group>
          <ul className="mt-3" style={{ listStyle: "none", padding: 0 }}>
            {files.length > 0 ? files.map((file, index) => <li key={index} style={{ padding: "5px 0", color: "#2BC6D1" }}>{file.name}</li>) : <li style={{ color: "#888" }}>No documents uploaded</li>}
          </ul>
        </Col>

        <Col md={9} className="p-4 d-flex flex-column h-100 animate__animated animate__fadeInRight" style={{ borderRadius: "0 20px 20px 0" }}>
          <h3 style={{ color: "#2BC6D1", fontFamily: "Zen Dots, sans-serif" }}><em>Evalumate</em></h3>
          <div ref={chatRef} className="flex-grow-1 overflow-auto p-4 rounded animate__animated animate__fadeIn" style={{ backgroundColor: "#1A1A1A", color: "#FFFFFF", borderRadius: "20px" }}>
            {messages.map((msg, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
                style={{ 
                  display: "flex",
                  justifyContent: msg.sender === "User" ? "flex-end" : "flex-start",
                  marginBottom: "15px",
                }}
              >
                <div 
                  style={{ 
                    maxWidth: "80%",
                    padding: "14px 20px",
                    borderRadius: "25px",
                    fontSize: "18px",
                    color: msg.sender === "User" ? "#fff" : "#000",
                    background: msg.sender === "User" 
                      ? "linear-gradient(to right, #2BC6D1, #28007B)" 
                      : "linear-gradient(to right, #f1f1f1, #e0e0e0)",
                    boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.3)",
                    position: "relative",
                  }}
                >
                  {msg.text}
                  <div style={{ fontSize: "12px", marginTop: "8px", textAlign: "right", opacity: 0.7 }}>
                    {msg.timestamp}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="p-3 mt-3 animate__animated animate__fadeInUp" style={{ backgroundColor: "#1A1A1A", borderRadius: "20px" }}>
            <InputGroup>
              <Form.Control
                as="textarea"
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type a message..."
                style={{ backgroundColor: "#000000", color: "#FFFFFF", borderColor: "#2BC6D1", borderRadius: "25px", fontFamily: "Oswald, sans-serif", fontSize: "16px", padding: "12px", resize: "none" }}
              />
              <Button style={{ backgroundColor: "#2BC6D1", color: "#000000", borderRadius: "15px", marginLeft: "3px" }} onClick={handleSendMessage}>
                <Send size={20} />
              </Button>
            </InputGroup>
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
