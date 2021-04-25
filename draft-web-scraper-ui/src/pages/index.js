import React, { useEffect, useState } from "react";
import highcarts from 'highcharts';

// styles
const pageStyles = {
  color: "#232129",
  padding: 50,
  fontFamily: "-apple-system, Roboto, sans-serif, serif",
}
const headingStyles = {
  marginTop: 0,
  marginBottom: 64,
  maxWidth: 320,
}
const headingAccentStyles = {
  color: "#663399",
}
const paragraphStyles = {
  marginBottom: 48,
}
const codeStyles = {
  color: "#8A6534",
  padding: 4,
  backgroundColor: "#FFF4DB",
  fontSize: "1.25rem",
  borderRadius: 4,
}
const listStyles = {
  marginBottom: 96,
  paddingLeft: 0,
}
const listItemStyles = {
  fontWeight: 300,
  fontSize: 24,
  maxWidth: 560,
  marginBottom: 30,
}

const linkStyle = {
  color: "#8954A8",
  fontWeight: "bold",
  fontSize: 16,
  verticalAlign: "5%",
}

const docLinkStyle = {
  ...linkStyle,
  listStyleType: "none",
  marginBottom: 24,
}

const descriptionStyle = {
  color: "#232129",
  fontSize: 14,
  marginTop: 10,
  marginBottom: 0,
  lineHeight: 1.25,
}


const badgeStyle = {
  color: "#fff",
  backgroundColor: "#088413",
  border: "1px solid #088413",
  fontSize: 11,
  fontWeight: "bold",
  letterSpacing: 1,
  borderRadius: 4,
  padding: "4px 6px",
  display: "inline-block",
  position: "relative",
  top: -2,
  marginLeft: 10,
  lineHeight: 1,
  cursor: 'pointer'
}


export default function Home() {
  const [players, setPlayers] = useState([])
  const [draftPosition, setDraftPosition] = useState()

  const getPlayersByPostiion = async () => {
    
    const response = await fetch(`https://w8a2bosl9k.execute-api.us-west-2.amazonaws.com/dev/draft/${draftPosition}`);
    const json = await response.json();

    setPlayers(json['body']);
  }

  const handleSetDraftPosition = (e) => {
    setDraftPosition(e.target.value)
  }

  return (
    <div style={pageStyles}>
      <div style={listItemStyles}>
        <input onChange={handleSetDraftPosition} value={draftPosition} />
        <buttom style={badgeStyle} onClick={getPlayersByPostiion}>Fetch</buttom>
      </div>
      {
        players.length ? players.map(player => {
          return (
            <div style={listItemStyles}>
              {player.player_name}, {player.player_position}, {player.player_team}
            </div>
          )
        }) : null
      }
    </div>
  )
}