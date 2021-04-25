import React, { useEffect, useState } from "react";
import Highcharts from 'highcharts';

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
    buildChart(json['body']);
  }

  const handleSetDraftPosition = (e) => {
    setDraftPosition(e.target.value)
  }

  const buildChart = (players) => {
    var _map = {}
    for (let i = 0; i < players.length; i++) {
      if (_map[players[i].player_name]) _map[players[i].player_name] += 1
      else _map[players[i].player_name] = 1
    }

    var categories = Object.keys(_map)
    var data = Object.values(_map)

    Highcharts.chart('container', {
      chart: {
        type: 'column'
      },
      title: {
        text: `Selection # ${players[0].position} (${players[0].team})`
      },
      subtitle: {
        text: ''
      },
      xAxis: {
        categories,
        crosshair: true
      },
      yAxis: {
        min: 0,
        title: {
          text: ''
        }
      },
      tooltip: {
        headerFormat: '<span>{point.key}</span><table>',
        pointFormat: '<tr><td>{series.name}: </td>' +
          '<td ><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
      },
      plotOptions: {
        series: {
          borderWidth: 0,
          dataSorting: {
            enabled: true
          },
        }
      },
      series: [{
        name: 'Number of Times Selected',
        data
      }]
    });
  }



  return (
    <div style={pageStyles}>
      <div style={listItemStyles}>
        <input onChange={handleSetDraftPosition} value={draftPosition} />
        <buttom style={badgeStyle} onClick={getPlayersByPostiion}>Fetch</buttom>
      </div>
      <div id="container"></div>
      {/* {
        players.length ? players.map(player => {
          return (
            <div style={listItemStyles}>
              {player.player_name}, {player.player_position}, {player.player_team}
            </div>
          )
        }) : null
      } */}
    </div>
  )
}