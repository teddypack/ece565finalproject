/*
Title: mypredictor
Author: Conor Green
Purpose: Final Project for ECE565
Description: Header file to provide definitions for mypredictor.cc
*/

#ifndef MYPREDICTOR_H
#define MYPREDICTOR_H

#include <stdint.h>
#include <stdio.h>

// Print helper inlines.
inline void printBinary(unsigned int number)
{
    if (number >> 1) {
        printBinary(number >> 1);
    }
    putc((number & 1) ? '1' : '0', stdout);
}

inline void printBinaryNumber(unsigned int number){
    printBinary(number);
    puts("\n");
}

static const unsigned int NUM_LOADS_TO_PREDICT = 100000;

static const int APT_SIZE = 1024;
static const int LOAD_PATH_REG_SIZE = 32;
static const int TAG_BIT_LENGTH = 14;
static const float CONFIDENCE_TRANSITION_VECTOR[3] = {1.0 , 0.5 , 0.25};

struct stats{
    uint32_t total = 0;
    uint32_t numCorrect = 0;
};

struct APTEntry{
    uint16_t tag = 0;
    uint64_t address = 0;
    uint8_t confidence = 0;
    uint8_t size = 0;
};

// extern stats myStats;
// extern APTEntry myAPT[APT_SIZE];
// extern uint32_t loadPathHistory;
// loadPathHistory = 0;

extern stats myStats;
extern APTEntry myAPT[APT_SIZE];
extern uint32_t loadPathHistory;
// loadPathHistory = 0;


void printBinary(unsigned int number);
void printBinaryNumber(unsigned int number);

void updateLoadPathHistory(uint64_t pc);

unsigned int calcAPTIndex(uint64_t pc);
unsigned int calcAPTTag(uint64_t pc);

bool queryAPTHitMiss(unsigned int index_raw);

APTEntry getAPTEntry(unsigned int index);
void setAPTEntry(unsigned int index, APTEntry entry);

uint8_t incrementConfidence(uint8_t old_conf);

APTEntry allocateNew(uint64_t address, uint64_t pc);

bool isCorrectPred(uint64_t &predictedAddr, uint64_t& actualAddr, uint64_t pc);

void updateStats(uint64_t &predictedAddr, uint64_t& actualAddr, uint64_t pc);

void printStats();
void printStatsWithLimit();

void trainAPT(uint64_t &predicted_val, uint64_t& actual_val, uint64_t pc);

bool getPrediction(uint64_t pc, uint64_t* predicted_value);

uint64_t getPredictionRaw(uint64_t pc);

//int main();

#endif