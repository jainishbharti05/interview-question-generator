import { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Select,
  VStack,
  useToast,
  Text,
  Tag,
  Input,
  IconButton,
  HStack,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Textarea,
  Divider,
} from '@chakra-ui/react';
import { AddIcon, CloseIcon } from '@chakra-ui/icons';
import { Domain, ExperienceLevel, Question } from '../types';
import { generateQuestions } from '../services/api';

const QuestionGenerator = () => {
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [requirements, setRequirements] = useState<string[]>(['']);
  const [experienceLevel, setExperienceLevel] = useState<ExperienceLevel>(ExperienceLevel.MID);
  const [domain, setDomain] = useState<Domain>(Domain.BACKEND);
  const [numQuestions, setNumQuestions] = useState(1);
  const [jobDescription, setJobDescription] = useState('');
  const toast = useToast();
  const extractRequirements = (jd: string) => {
    const lines = jd.split('\n');
    const requirements: string[] = [];
    
    // Common requirement indicators
    const bulletPoints = /^[\-•\*\d\.\s]+/;
    const requirementKeywords = [
      'experience with',
      'knowledge of',
      'familiar with',
      'proficiency in',
      'proficient in',
      'understanding of',
      'ability to',
      'skills in',
      'expertise in',
      'background in',
      'required:',
      'requirements:',
      'qualifications:',
      'must have',
      'responsible for',
      'will be',
      'you have',
      'you\'ll need',
      'proven track record',
      'demonstrated experience',
      'strong understanding',
      'deep knowledge',
      'hands-on experience',
      'experience building',
      'experience developing',
    ];

    // Common tech stack keywords
    const techKeywords = new Set([
      'react', 'angular', 'vue', 'javascript', 'typescript', 'node', 'express', 
      'python', 'django', 'flask', 'fastapi', 'java', 'spring', 'c#', '.net',
      'php', 'laravel', 'ruby', 'rails', 'go', 'rust', 'sql', 'mongodb', 'postgresql',
      'mysql', 'redis', 'elasticsearch', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
      'graphql', 'rest', 'kafka', 'rabbitmq', 'jenkins', 'github', 'gitlab', 'ci/cd',
      'react native', 'flutter', 'swift', 'kotlin', 'android', 'ios'
    ]);

    let inRequirementsList = false;
    let continuedLine = '';
    const seenRequirements = new Set<string>();
    
    // Helper function to normalize and deduplicate requirements
    const addRequirement = (text: string) => {
      // Clean up the text
      text = text.replace(/[,.;]$/, '').trim();
      
      // Skip if too short or already seen
      if (text.length < 10 || seenRequirements.has(text.toLowerCase())) {
        return;
      }

      // Normalize text and store lowercase version for deduplication
      seenRequirements.add(text.toLowerCase());
      requirements.push(text);
    };

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i].trim();
      if (!line) {
        if (continuedLine) {
          addRequirement(continuedLine);
          continuedLine = '';
        }
        continue;
      }
      
      // Check for section headers that indicate requirements
      const lowerLine = line.toLowerCase();
      if (lowerLine.match(/^(requirements|qualifications|what you['']ll need|what we['']re looking for|key skills|technical skills|about you|you will have|your background|role requirements|technical requirements|skills required|minimum qualifications|preferred qualifications):/)) {
        inRequirementsList = true;
        if (continuedLine) {
          addRequirement(continuedLine);
          continuedLine = '';
        }
        continue;
      }
      
      // Process bullets and numbered items
      if (line.match(bulletPoints) || inRequirementsList) {
        // If we have a continued line from before, add it now
        if (continuedLine) {
          addRequirement(continuedLine);
          continuedLine = '';
        }

        line = line.replace(bulletPoints, '').trim();
        
        // Check if this line might continue in the next line
        const nextLine = i < lines.length - 1 ? lines[i + 1].trim() : '';
        if (nextLine && !nextLine.match(bulletPoints) && !nextLine.match(/^[A-Z]/)) {
          continuedLine = line + ' ' + nextLine;
          i++; // Skip the next line since we've incorporated it
        } else {
          addRequirement(line);
        }
        continue;
      }
      
      // Look for requirement keywords
      if (requirementKeywords.some(keyword => lowerLine.includes(keyword))) {
        addRequirement(line);
        continue;
      }
      
      // Look for technology stacks and programming languages
      const techStackMatch = line.match(/(?:using|with|in)\s+([A-Za-z0-9\s,/.#+]+)(?:\s+(?:and|or)\s+[A-Za-z0-9\s,/.#+]+)?/i);
      if (techStackMatch) {
        const technologies = techStackMatch[1].toLowerCase()
          .split(/[,\s]+(?:and|or|\s)*/)
          .map(t => t.trim())
          .filter(t => techKeywords.has(t));
        
        if (technologies.length > 0) {
          const techList = technologies.join(', ');
          addRequirement(`Experience with ${techList}`);
        }
      }
    }

    // Handle any remaining continued line
    if (continuedLine) {
      addRequirement(continuedLine);
    }
    
    // Update state and show toast notification
    if (requirements.length > 0) {
      setRequirements(requirements);
      toast({
        title: 'Requirements Extracted',
        description: `Found ${requirements.length} requirements from the job description`,
        status: 'success',
        duration: 3000,
      });
    } else {
      setRequirements(['']);
      toast({
        title: 'No Requirements Found',
        description: 'Please enter requirements manually or adjust the job description',
        status: 'warning',
        duration: 3000,
      });
    }
  };

  const handleJDChange = (value: string) => {
    setJobDescription(value);
    // Auto-extract if the JD is long enough
    if (value.length > 50) {
      extractRequirements(value);
    }
  };

  const handleAddRequirement = () => {
    setRequirements([...requirements, '']);
  };

  const handleRemoveRequirement = (index: number) => {
    const newRequirements = requirements.filter((_, i) => i !== index);
    setRequirements(newRequirements);
  };

  const handleRequirementChange = (index: number, value: string) => {
    const newRequirements = [...requirements];
    newRequirements[index] = value;
    setRequirements(newRequirements);
  };

  const handleSubmit = async () => {
    const validRequirements = requirements.filter(req => req.trim() !== '');
    if (validRequirements.length === 0) {
      toast({
        title: 'Error',
        description: 'Please add at least one job requirement',
        status: 'error',
        duration: 3000,
      });
      return;
    }

    setLoading(true);
    try {
      const response = await generateQuestions({
        job_requirements: validRequirements,
        experience_level: experienceLevel,
        domain,
        num_questions: numQuestions,
      });
      setQuestions(response.questions);
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to generate questions',
        status: 'error',
        duration: 5000,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <VStack spacing={6} align="stretch">
        {/* Job Description Textarea */}
        <FormControl>
          <FormLabel>Job Description</FormLabel>
          <Textarea
            value={jobDescription}
            onChange={(e) => handleJDChange(e.target.value)}
            placeholder="Paste the full job description here..."
            minHeight="200px"
            mb={2}
          />
          <Button
            size="sm"
            onClick={() => extractRequirements(jobDescription)}
            isDisabled={!jobDescription}
            colorScheme="teal"
          >
            Extract Requirements
          </Button>
        </FormControl>

        <Divider />

        {/* Extracted Requirements */}
        <FormControl>
          <FormLabel>Extracted Requirements (edit as needed)</FormLabel>
          {requirements.map((req, index) => (
            <HStack key={index} mb={2}>
              <Input
                value={req}
                onChange={(e) => handleRequirementChange(index, e.target.value)}
                placeholder="Enter a job requirement"
              />
              {requirements.length > 1 && (
                <IconButton
                  aria-label="Remove requirement"
                  icon={<CloseIcon />}
                  onClick={() => handleRemoveRequirement(index)}
                  colorScheme="red"
                  size="sm"
                />
              )}
            </HStack>
          ))}
          <Button
            leftIcon={<AddIcon />}
            onClick={() => setRequirements([...requirements, ''])}
            size="sm"
            mt={2}
          >
            Add Requirement
          </Button>
        </FormControl>

        {/* Experience Level */}
        <FormControl>
          <FormLabel>Experience Level</FormLabel>
          <Select
            value={experienceLevel}
            onChange={(e) => setExperienceLevel(e.target.value as ExperienceLevel)}
          >
            {Object.entries(ExperienceLevel).map(([key, value]) => (
              <option key={key} value={value}>
                {key.charAt(0) + key.slice(1).toLowerCase()}
              </option>
            ))}
          </Select>
        </FormControl>

        {/* Domain */}
        <FormControl>
          <FormLabel>Domain</FormLabel>
          <Select
            value={domain}
            onChange={(e) => setDomain(e.target.value as Domain)}
          >
            {Object.entries(Domain).map(([key, value]) => (
              <option key={key} value={value}>
                {key.split('_').map(word => word.charAt(0) + word.slice(1).toLowerCase()).join(' ')}
              </option>
            ))}
          </Select>
        </FormControl>

        {/* Number of Questions */}
        <FormControl>
          <FormLabel>Number of Questions</FormLabel>
          <NumberInput
            min={1}
            max={5}
            value={numQuestions}
            onChange={(_, value) => setNumQuestions(value)}
          >
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        </FormControl>

        {/* Generate Button */}
        <Button
          colorScheme="blue"
          onClick={handleSubmit}
          isLoading={loading}
          loadingText="Generating..."
          size="lg"
        >
          Generate Questions
        </Button>

        {/* Generated Questions */}
        {questions.map((q, index) => (
          <Box
            key={index}
            p={6}
            borderWidth="1px"
            borderRadius="lg"
            boxShadow="sm"
            bg="white"
          >
            <HStack spacing={2} mb={4}>
              <Tag size="md" colorScheme="blue">
                {q.skill_area}
              </Tag>
              <Tag size="md" colorScheme={q.difficulty > 7 ? 'red' : q.difficulty > 4 ? 'yellow' : 'green'}>
                Difficulty: {q.difficulty}/10
              </Tag>
            </HStack>
            
            <Text fontSize="lg" fontWeight="bold" mb={4}>
              {q.question}
            </Text>

            <Text fontWeight="bold" mb={2}>
              Evaluation Criteria:
            </Text>
            <VStack align="stretch" spacing={1} mb={4}>
              {q.evaluation_criteria.map((criterion, idx) => (
                <Text key={idx}>• {criterion}</Text>
              ))}
            </VStack>

            <Text fontWeight="bold" mb={2}>
              Example Answer:
            </Text>
            <Text whiteSpace="pre-wrap">{q.example_answer}</Text>
          </Box>
        ))}
      </VStack>
    </Box>
  );
};

export default QuestionGenerator;
