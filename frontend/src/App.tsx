import { ChakraProvider, Container, Heading } from '@chakra-ui/react';
import QuestionGenerator from './components/QuestionGenerator.tsx';

function App() {
  return (
    <ChakraProvider>
      <Container maxW="container.xl" py={8}>
        <Heading mb={8} textAlign="center">
          Technical Interview Question Generator
        </Heading>
        <QuestionGenerator />
      </Container>
    </ChakraProvider>
  )
}

export default App;
