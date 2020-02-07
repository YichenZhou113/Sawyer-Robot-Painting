// Auto-generated. Do not edit!

// (in-package planning.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class ChouChou {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.position_x = null;
      this.position_y = null;
      this.position_z = null;
      this.edge_grad = null;
      this.status_type = null;
      this.pen_type = null;
    }
    else {
      if (initObj.hasOwnProperty('position_x')) {
        this.position_x = initObj.position_x
      }
      else {
        this.position_x = 0.0;
      }
      if (initObj.hasOwnProperty('position_y')) {
        this.position_y = initObj.position_y
      }
      else {
        this.position_y = 0.0;
      }
      if (initObj.hasOwnProperty('position_z')) {
        this.position_z = initObj.position_z
      }
      else {
        this.position_z = 0.0;
      }
      if (initObj.hasOwnProperty('edge_grad')) {
        this.edge_grad = initObj.edge_grad
      }
      else {
        this.edge_grad = 0.0;
      }
      if (initObj.hasOwnProperty('status_type')) {
        this.status_type = initObj.status_type
      }
      else {
        this.status_type = '';
      }
      if (initObj.hasOwnProperty('pen_type')) {
        this.pen_type = initObj.pen_type
      }
      else {
        this.pen_type = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ChouChou
    // Serialize message field [position_x]
    bufferOffset = _serializer.float64(obj.position_x, buffer, bufferOffset);
    // Serialize message field [position_y]
    bufferOffset = _serializer.float64(obj.position_y, buffer, bufferOffset);
    // Serialize message field [position_z]
    bufferOffset = _serializer.float64(obj.position_z, buffer, bufferOffset);
    // Serialize message field [edge_grad]
    bufferOffset = _serializer.float64(obj.edge_grad, buffer, bufferOffset);
    // Serialize message field [status_type]
    bufferOffset = _serializer.string(obj.status_type, buffer, bufferOffset);
    // Serialize message field [pen_type]
    bufferOffset = _serializer.int64(obj.pen_type, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ChouChou
    let len;
    let data = new ChouChou(null);
    // Deserialize message field [position_x]
    data.position_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [position_y]
    data.position_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [position_z]
    data.position_z = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [edge_grad]
    data.edge_grad = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [status_type]
    data.status_type = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [pen_type]
    data.pen_type = _deserializer.int64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.status_type.length;
    return length + 44;
  }

  static datatype() {
    // Returns string type for a message object
    return 'planning/ChouChou';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f61e71bd64cbb15ad5eb3947b804986d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 position_x
    float64 position_y
    float64 position_z
    float64 edge_grad
    string status_type
    int64 pen_type
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ChouChou(null);
    if (msg.position_x !== undefined) {
      resolved.position_x = msg.position_x;
    }
    else {
      resolved.position_x = 0.0
    }

    if (msg.position_y !== undefined) {
      resolved.position_y = msg.position_y;
    }
    else {
      resolved.position_y = 0.0
    }

    if (msg.position_z !== undefined) {
      resolved.position_z = msg.position_z;
    }
    else {
      resolved.position_z = 0.0
    }

    if (msg.edge_grad !== undefined) {
      resolved.edge_grad = msg.edge_grad;
    }
    else {
      resolved.edge_grad = 0.0
    }

    if (msg.status_type !== undefined) {
      resolved.status_type = msg.status_type;
    }
    else {
      resolved.status_type = ''
    }

    if (msg.pen_type !== undefined) {
      resolved.pen_type = msg.pen_type;
    }
    else {
      resolved.pen_type = 0
    }

    return resolved;
    }
};

module.exports = ChouChou;
