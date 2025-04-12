"use client"

import type React from "react"
import { useState } from "react"
import { TextField, Button, Typography, Paper, Box } from "@mui/material"

const UserProfile: React.FC = () => {
  const [abhaId, setAbhaId] = useState("")
  const [name, setName] = useState("")
  const [age, setAge] = useState("")
  const [gender, setGender] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Implement ABHA verification and profile update logic here
    console.log("Profile updated:", { abhaId, name, age, gender })
  }

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 400, mx: "auto" }}>
      <Typography variant="h5" gutterBottom>
        User Profile
      </Typography>
      <Box component="form" onSubmit={handleSubmit}>
        <TextField
          fullWidth
          label="ABHA ID"
          value={abhaId}
          onChange={(e) => setAbhaId(e.target.value)}
          margin="normal"
        />
        <TextField fullWidth label="Name" value={name} onChange={(e) => setName(e.target.value)} margin="normal" />
        <TextField
          fullWidth
          label="Age"
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          margin="normal"
        />
        <TextField
          fullWidth
          label="Gender"
          value={gender}
          onChange={(e) => setGender(e.target.value)}
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
          Update Profile
        </Button>
      </Box>
    </Paper>
  )
}

export default UserProfile

