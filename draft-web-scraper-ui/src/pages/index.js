import React, { useEffect, useState } from "react";
import highcarts from 'highcharts';


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


  useEffect(() => {

  })

  return (
    <div>
      <input onChange={handleSetDraftPosition} value={draftPosition} onBlur={getPlayersByPostiion}/>
      {
        players.length ? players.map(player => {
          return (
            <div>
              {player.player_name}
            </div>
          )
        }) : null
      }
    </div>
  )
}