################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../src/ReceiverSS.cpp \
../src/SenderSS.cpp 

OBJS += \
./src/ReceiverSS.o \
./src/SenderSS.o 

CPP_DEPS += \
./src/ReceiverSS.d \
./src/SenderSS.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -I"/media/sf_ENSC_Share/Ensc351Part3/Ensc351x-myio" -I"/media/sf_ENSC_Share/Ensc351Part3/Ensc351xmodem" -I"/media/sf_ENSC_Share/Ensc351Part3/Ensc351" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


