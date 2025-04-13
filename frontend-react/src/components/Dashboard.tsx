"use client"

import type React from "react"
import { useState } from "react"
import { Box, Container, Grid, Paper, Typography, AppBar, Toolbar } from "@mui/material"
import { motion } from "framer-motion"
import dynamic from "next/dynamic"
import Sidebar from "./Sidebar"
import SymptomForm from "./SymptomForm"
import DiagnosisResult from "./DiagnosisResult"

// Dynamically import components that might use browser-specific APIs
const DynamicHealthLibrary = dynamic(() => import("./HealthLibrary"), { ssr: false })
const DynamicTeleconsultation = dynamic(() => import("./Teleconsultation"), { ssr: false })
const DynamicUserProfile = dynamic(() => import("./UserProfile"), { ssr: false })

const Dashboard: React.FC = () => {
  const [diagnosis, setDiagnosis] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState("home")

  const handleSymptomSubmit = async (symptoms: string, language: string) => {
    try {
      const response = await fetch("http://localhost:5000/api/diagnose", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ symptoms, language }),
      })
      const data = await response.json()
      setDiagnosis(data.diagnosis)
    } catch (error) {
      console.error("Error getting diagnosis:", error)
      setDiagnosis("An error occurred while getting the diagnosis. Please try again.")
    }
  }

  const renderContent = () => {
    switch (currentPage) {
      case "home":
        return (
          <Grid container spacing={3}>
            <Grid component="div" item xs={12} md={6}>
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
                <Paper elevation={3} sx={{ p: 3 }}>
                  <SymptomForm handleSubmit={handleSymptomSubmit} />
                </Paper>
              </motion.div>
            </Grid>
            <Grid item xs={12} md={6}>
              {diagnosis && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                >
                  <DiagnosisResult result={diagnosis} />
                </motion.div>
              )}
            </Grid>
          </Grid>
        )
      case "library":
        return <DynamicHealthLibrary />
      case "teleconsultation":
        return <DynamicTeleconsultation />
      case "profile":
        return <DynamicUserProfile />
      default:
        return null
    }
  }

  return (
    <Box sx={{ display: "flex" }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            AI Health Diagnostic Kiosk
          </Typography>
        </Toolbar>
      </AppBar>
      <Sidebar onNavigate={setCurrentPage} />
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Container maxWidth="lg">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
            {renderContent()}
          </motion.div>
        </Container>
      </Box>
    </Box>
  )
}

export default Dashboard

