"use client"

import type React from "react"
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Box } from "@mui/material"
import { Home, LocalHospital, VideoCall, Person } from "@mui/icons-material"

const drawerWidth = 240

interface SidebarProps {
  onNavigate: (page: string) => void
}

const Sidebar: React.FC<SidebarProps> = ({ onNavigate }) => {
  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
          backgroundColor: "#f8f9fa",
          borderRight: "1px solid #e0e0e0",
        },
      }}
      variant="permanent"
      anchor="left"
    >
      <Toolbar />
      <Box sx={{ overflow: "auto", mt: 2 }}>
        <List>
          {[
            { text: "Home", icon: <Home />, page: "home" },
            { text: "Health Library", icon: <LocalHospital />, page: "library" },
            { text: "Teleconsultation", icon: <VideoCall />, page: "teleconsultation" },
            { text: "Profile", icon: <Person />, page: "profile" },
          ].map((item) => (
            <ListItem component="div"
              button
              key={item.text}
              onClick={() => onNavigate(item.page)}
              sx={{
                "&:hover": {
                  backgroundColor: "rgba(0, 0, 0, 0.04)",
                },
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  )
}

export default Sidebar

