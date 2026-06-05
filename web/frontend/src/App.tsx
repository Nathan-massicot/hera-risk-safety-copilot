import { Navigate, Route, Routes } from "react-router-dom";
import Login from "./auth/Login";
import Register from "./auth/Register";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Chatbot from "./pages/Chatbot";
import DecisionTree from "./pages/DecisionTree";
import RegulationDiagram from "./pages/RegulationDiagram";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        path="/diagram"
        element={
          <ProtectedRoute>
            <Layout>
              <RegulationDiagram />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/decision-tree"
        element={
          <ProtectedRoute>
            <Layout>
              <DecisionTree />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/chat"
        element={
          <ProtectedRoute>
            <Layout>
              <Chatbot />
            </Layout>
          </ProtectedRoute>
        }
      />

      <Route path="/" element={<Navigate to="/chat" replace />} />
      <Route path="*" element={<Navigate to="/chat" replace />} />
    </Routes>
  );
}
