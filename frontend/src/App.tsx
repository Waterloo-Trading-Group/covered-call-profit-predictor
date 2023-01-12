import * as React from "react"
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Grid,
  theme,
  Button,
  Input,
  NumberInput,
  NumberInputField,
} from "@chakra-ui/react"
import { ColorModeSwitcher } from "./ColorModeSwitcher"
import { Logo } from "./Logo"
import axios from 'axios'



export const App = () => {

  const [ticker, setTicker] = React.useState('')
  const [daysTillStrike, setDaysTillStirke] = React.useState(0)
  const [premium, setPremium] = React.useState(0)
  const [strikePrice, setStrikePrice] = React.useState(0)
  const [profit, setProfit] = React.useState('')

  async function getProfit(ticker: string, daysTillStrike: number, premium: number, strikePrice: number) {
  
    axios.get('http://127.0.0.1:8000/' + ticker + '/' + daysTillStrike.toString() + '/' + premium.toString() + '/' + strikePrice.toString())
    .then((response: { data: any }) => {
      const data = response.data;
      const profitd = data['Message'];
      setProfit(profitd);
      console.log(data);
    })
    .catch((error: any) => {
      console.log(error);
    });
  }

  return (
    <ChakraProvider theme={theme}>
      <div className="App">
          <Input width='auto' min={0} max={100}  type="text" placeholder='Ticker' onChange={(e) => setTicker(e.target.value)} />
          <NumberInput width='auto' defaultValue={0} onChange={(valueString) => setDaysTillStirke(parseInt(valueString))}>
            <NumberInputField />
          </NumberInput>
          <NumberInput width='auto' defaultValue={0}  onChange={(valueString) => setPremium(parseInt(valueString))}>
            <NumberInputField />
          </NumberInput>
          <NumberInput width='auto' defaultValue={0} onChange={(valueString) => setStrikePrice(parseInt(valueString))}>
            <NumberInputField />
          </NumberInput>
          <Button onClick={() => getProfit(ticker, daysTillStrike, premium, strikePrice)}>Get Data</Button>
          <p>{profit}</p>
      </div>
    </ChakraProvider>
  )
}
