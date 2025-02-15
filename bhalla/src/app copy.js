import cors from "cors";
import express from "express";


const app = express();
app.use(cors({
    origin: process.env.CORS_ORIGIN,
    credentials: true
}));
app.use(express.json()); // For parsing application/json
app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));
export { app };
