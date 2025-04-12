"use client"

import type React from "react"
import { Grid, Card, CardContent, CardMedia, Typography, Button } from "@mui/material"

const healthArticles = [
  {
    title: "Understanding Diabetes",
    description: "Learn about the causes, symptoms, and management of diabetes.",
    image: "https://via.placeholder.com/300x200?text=Diabetes",
  },
  {
    title: "Heart Health Basics",
    description: "Discover key factors for maintaining a healthy heart.",
    image: "https://via.placeholder.com/300x200?text=Heart+Health",
  },
  {
    title: "Nutrition and Diet",
    description: "Explore the fundamentals of a balanced and nutritious diet.",
    image: "https://via.placeholder.com/300x200?text=Nutrition",
  },
  // Add more health articles as needed
]

const HealthLibrary: React.FC = () => {
  return (
    <div>
      <Typography variant="h5" gutterBottom>
        Health Information Library
      </Typography>
      <Grid container spacing={3}>
        {healthArticles.map((article, index) => (
          <Grid component="div" item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardMedia component="img" height="140" image={article.image} alt={article.title} />
              <CardContent>
                <Typography gutterBottom variant="h6" component="div">
                  {article.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {article.description}
                </Typography>
                <Button size="small" color="primary" sx={{ mt: 1 }}>
                  Read More
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  )
}

export default HealthLibrary

