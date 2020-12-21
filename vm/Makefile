TARGET_EXEC ?= lob

BUILD_DIR ?= ./build
SRC_DIR ?= ./src
INC_DIR ?= ./include

SRCS := $(shell find $(SRC_DIR) -name *.cpp)
OBJS := $(SRCS:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)

$(info $(OBJS))
$(info $(BUILD_DIR))

INC_FLAGS := $(addprefix -I,$(INC_DIR))

CPPFLAGS ?= $(INC_FLAGS)

$(BUILD_DIR)/$(TARGET_EXEC): $(OBJS)
	$(CXX) $(OBJS) -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(MKDIR_P) $(dir $@)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@


.PHONY: clean

clean:
	$(RM) -r $(BUILD_DIR)

MKDIR_P ?= mkdir -p
