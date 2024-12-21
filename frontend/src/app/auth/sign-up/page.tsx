'use client';

/* eslint-disable */
/**
  Horizon UI Sign-Up Page
  Modified for user registration purposes.
**/

import React, { useRef, useState } from 'react';
// Chakra imports
import {
  Box,
  Button,
  Checkbox,
  Flex,
  FormControl,
  FormLabel,
  Heading,
  Icon,
  Input,
  InputGroup,
  InputRightElement,
  Text,
  useColorModeValue,
} from '@chakra-ui/react';
// Custom components
import { HSeparator } from 'components/separator/Separator';
import DefaultAuthLayout from 'layouts/auth/Default';
// Assets
import Link from 'next/link';
import { MdOutlineRemoveRedEye } from 'react-icons/md';
import { RiEyeCloseLine } from 'react-icons/ri';

export default function SignUp() {
  // Chakra color mode
  const textColor = useColorModeValue('navy.700', 'white');
  const textColorSecondary = 'gray.400';
  const textColorDetails = useColorModeValue('navy.700', 'secondaryGray.600');
  const textColorBrand = useColorModeValue('brand.500', 'white');
  const brandStars = useColorModeValue('brand.500', 'brand.400');

  const [show, setShow] = useState(false);
  const handleClick = () => setShow(!show);

  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const confirmPasswordRef = useRef<HTMLInputElement>(null);
  const firstNameRef = useRef<HTMLInputElement>(null);
  const lastNameRef = useRef<HTMLInputElement>(null);
  const mobileRef = useRef<HTMLInputElement>(null);

  const handleSignUp = async () => {
    const email = emailRef.current?.value;
    const password = passwordRef.current?.value;
    const confirmPassword = confirmPasswordRef.current?.value;
    const first_name = firstNameRef.current?.value;
    const last_name = lastNameRef.current?.value;
    const mobile = mobileRef.current?.value;

    if (!email || !password || !confirmPassword || !first_name || !last_name || !mobile) {
      alert('All fields are required.');
      return;
    }

    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    const url = 'http://localhost:8000/api/v1/users/signup';

    const options = {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        first_name,
        last_name,
        mobile,
      }),
    };

    try {
      const response = await fetch(url, options);
      const data = await response.json();

      if (response.ok) {
        alert('Account created successfully!');
      } else {
        alert(`Sign-Up failed: ${data.message || 'Unknown error'}`);
      }
    } catch (error) {
      alert('An error occurred during sign-up. Please try again later.');
      console.error('Error:', error);
    }
  };

  return (
    <DefaultAuthLayout illustrationBackground={'/img/auth/auth.png'}>
      <Flex
        maxW={{ base: '100%', md: 'max-content' }}
        w="100%"
        mx={{ base: 'auto', lg: '0px' }}
        me="auto"
        h="100%"
        alignItems="start"
        justifyContent="center"
        mb={{ base: '30px', md: '60px' }}
        px={{ base: '25px', md: '0px' }}
        mt={{ base: '40px', md: '14vh' }}
        flexDirection="column"
      >
        <Box me="auto">
          <Heading color={textColor} fontSize="36px" mb="10px">
            Sign Up
          </Heading>
          <Text
            mb="36px"
            ms="4px"
            color={textColorSecondary}
            fontWeight="400"
            fontSize="md"
          >
            Enter your details to create a new account!
          </Text>
        </Box>
        <Flex
          zIndex="2"
          direction="column"
          w={{ base: '100%', md: '420px' }}
          maxW="100%"
          background="transparent"
          borderRadius="15px"
          mx={{ base: 'auto', lg: 'unset' }}
          me="auto"
          mb={{ base: '20px', md: 'auto' }}
        >
          <FormControl>
            <FormLabel color={textColor} fontSize="sm" fontWeight="500">
              First Name<Text color={brandStars}>*</Text>
            </FormLabel>
            <Input
              ref={firstNameRef}
              type="text"
              placeholder="John"
              variant="auth"
              size="lg"
              mb="24px"
            />

            <FormLabel color={textColor} fontSize="sm" fontWeight="500">
              Last Name<Text color={brandStars}>*</Text>
            </FormLabel>
            <Input
              ref={lastNameRef}
              type="text"
              placeholder="Doe"
              variant="auth"
              size="lg"
              mb="24px"
            />

            <FormLabel color={textColor} fontSize="sm" fontWeight="500">
              Mobile<Text color={brandStars}>*</Text>
            </FormLabel>
            <Input
              ref={mobileRef}
              type="text"
              placeholder="123-456-7890"
              variant="auth"
              size="lg"
              mb="24px"
            />

            <FormLabel color={textColor} fontSize="sm" fontWeight="500">
              Email<Text color={brandStars}>*</Text>
            </FormLabel>
            <Input
              ref={emailRef}
              type="email"
              placeholder="mail@domain.com"
              variant="auth"
              size="lg"
              mb="24px"
            />

            <FormLabel color={textColor} fontSize="sm" fontWeight="500">
              Password<Text color={brandStars}>*</Text>
            </FormLabel>
            <InputGroup size="md">
              <Input
                ref={passwordRef}
                type={show ? 'text' : 'password'}
                placeholder="Min. 8 characters"
                variant="auth"
                size="lg"
                mb="24px"
              />
              <InputRightElement>
                <Icon
                  as={show ? RiEyeCloseLine : MdOutlineRemoveRedEye}
                  onClick={handleClick}
                  cursor="pointer"
                />
              </InputRightElement>
            </InputGroup>

            <FormLabel color={textColor} fontSize="sm" fontWeight="500">
              Confirm Password<Text color={brandStars}>*</Text>
            </FormLabel>
            <InputGroup size="md">
              <Input
                ref={confirmPasswordRef}
                type={show ? 'text' : 'password'}
                placeholder="Re-enter your password"
                variant="auth"
                size="lg"
                mb="24px"
              />
              <InputRightElement>
                <Icon
                  as={show ? RiEyeCloseLine : MdOutlineRemoveRedEye}
                  onClick={handleClick}
                  cursor="pointer"
                />
              </InputRightElement>
            </InputGroup>

            <Flex alignItems="center" mb="24px">
              <Checkbox id="terms-and-conditions" />
              <FormLabel
                htmlFor="terms-and-conditions"
                mb="0"
                fontSize="sm"
                fontWeight="normal"
              >
                I agree to the terms and conditions
              </FormLabel>
            </Flex>

            <Button w="100%" h="50px" onClick={handleSignUp}>
              Sign Up
            </Button>
          </FormControl>

          <Flex justifyContent="center" mt="20px">
            <Link href="/auth/sign-in">
              <Text>
                Already have an account?{' '}
                <Text as="span" color={textColorBrand} fontWeight="500">
                  Sign In
                </Text>
              </Text>
            </Link>
          </Flex>
        </Flex>
      </Flex>
    </DefaultAuthLayout>
  );
}
