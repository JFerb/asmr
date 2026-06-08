// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interfaces:action/SetVelocity.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_robot_interfaces/action/set_velocity.hpp"


#ifndef MY_ROBOT_INTERFACES__ACTION__DETAIL__SET_VELOCITY__BUILDER_HPP_
#define MY_ROBOT_INTERFACES__ACTION__DETAIL__SET_VELOCITY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interfaces/action/detail/set_velocity__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_Goal_angular_z
{
public:
  explicit Init_SetVelocity_Goal_angular_z(::my_robot_interfaces::action::SetVelocity_Goal & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::action::SetVelocity_Goal angular_z(::my_robot_interfaces::action::SetVelocity_Goal::_angular_z_type arg)
  {
    msg_.angular_z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_Goal msg_;
};

class Init_SetVelocity_Goal_linear_x
{
public:
  Init_SetVelocity_Goal_linear_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetVelocity_Goal_angular_z linear_x(::my_robot_interfaces::action::SetVelocity_Goal::_linear_x_type arg)
  {
    msg_.linear_x = std::move(arg);
    return Init_SetVelocity_Goal_angular_z(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_Goal>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_Goal_linear_x();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_Result_stopped
{
public:
  Init_SetVelocity_Result_stopped()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_robot_interfaces::action::SetVelocity_Result stopped(::my_robot_interfaces::action::SetVelocity_Result::_stopped_type arg)
  {
    msg_.stopped = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_Result>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_Result_stopped();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_Feedback_current_angular_z
{
public:
  explicit Init_SetVelocity_Feedback_current_angular_z(::my_robot_interfaces::action::SetVelocity_Feedback & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::action::SetVelocity_Feedback current_angular_z(::my_robot_interfaces::action::SetVelocity_Feedback::_current_angular_z_type arg)
  {
    msg_.current_angular_z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_Feedback msg_;
};

class Init_SetVelocity_Feedback_current_linear_x
{
public:
  Init_SetVelocity_Feedback_current_linear_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetVelocity_Feedback_current_angular_z current_linear_x(::my_robot_interfaces::action::SetVelocity_Feedback::_current_linear_x_type arg)
  {
    msg_.current_linear_x = std::move(arg);
    return Init_SetVelocity_Feedback_current_angular_z(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_Feedback>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_Feedback_current_linear_x();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_SendGoal_Request_goal
{
public:
  explicit Init_SetVelocity_SendGoal_Request_goal(::my_robot_interfaces::action::SetVelocity_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Request goal(::my_robot_interfaces::action::SetVelocity_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Request msg_;
};

class Init_SetVelocity_SendGoal_Request_goal_id
{
public:
  Init_SetVelocity_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetVelocity_SendGoal_Request_goal goal_id(::my_robot_interfaces::action::SetVelocity_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_SetVelocity_SendGoal_Request_goal(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_SendGoal_Request>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_SendGoal_Request_goal_id();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_SendGoal_Response_stamp
{
public:
  explicit Init_SetVelocity_SendGoal_Response_stamp(::my_robot_interfaces::action::SetVelocity_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Response stamp(::my_robot_interfaces::action::SetVelocity_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Response msg_;
};

class Init_SetVelocity_SendGoal_Response_accepted
{
public:
  Init_SetVelocity_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetVelocity_SendGoal_Response_stamp accepted(::my_robot_interfaces::action::SetVelocity_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_SetVelocity_SendGoal_Response_stamp(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_SendGoal_Response>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_SendGoal_Response_accepted();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_SendGoal_Event_response
{
public:
  explicit Init_SetVelocity_SendGoal_Event_response(::my_robot_interfaces::action::SetVelocity_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Event response(::my_robot_interfaces::action::SetVelocity_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Event msg_;
};

class Init_SetVelocity_SendGoal_Event_request
{
public:
  explicit Init_SetVelocity_SendGoal_Event_request(::my_robot_interfaces::action::SetVelocity_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_SetVelocity_SendGoal_Event_response request(::my_robot_interfaces::action::SetVelocity_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_SetVelocity_SendGoal_Event_response(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Event msg_;
};

class Init_SetVelocity_SendGoal_Event_info
{
public:
  Init_SetVelocity_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetVelocity_SendGoal_Event_request info(::my_robot_interfaces::action::SetVelocity_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_SetVelocity_SendGoal_Event_request(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_SendGoal_Event>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_SendGoal_Event_info();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_GetResult_Request_goal_id
{
public:
  Init_SetVelocity_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_robot_interfaces::action::SetVelocity_GetResult_Request goal_id(::my_robot_interfaces::action::SetVelocity_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_GetResult_Request>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_GetResult_Request_goal_id();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_GetResult_Response_result
{
public:
  explicit Init_SetVelocity_GetResult_Response_result(::my_robot_interfaces::action::SetVelocity_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::action::SetVelocity_GetResult_Response result(::my_robot_interfaces::action::SetVelocity_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_GetResult_Response msg_;
};

class Init_SetVelocity_GetResult_Response_status
{
public:
  Init_SetVelocity_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetVelocity_GetResult_Response_result status(::my_robot_interfaces::action::SetVelocity_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_SetVelocity_GetResult_Response_result(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_GetResult_Response>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_GetResult_Response_status();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_GetResult_Event_response
{
public:
  explicit Init_SetVelocity_GetResult_Event_response(::my_robot_interfaces::action::SetVelocity_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::action::SetVelocity_GetResult_Event response(::my_robot_interfaces::action::SetVelocity_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_GetResult_Event msg_;
};

class Init_SetVelocity_GetResult_Event_request
{
public:
  explicit Init_SetVelocity_GetResult_Event_request(::my_robot_interfaces::action::SetVelocity_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_SetVelocity_GetResult_Event_response request(::my_robot_interfaces::action::SetVelocity_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_SetVelocity_GetResult_Event_response(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_GetResult_Event msg_;
};

class Init_SetVelocity_GetResult_Event_info
{
public:
  Init_SetVelocity_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetVelocity_GetResult_Event_request info(::my_robot_interfaces::action::SetVelocity_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_SetVelocity_GetResult_Event_request(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_GetResult_Event>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_GetResult_Event_info();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace action
{

namespace builder
{

class Init_SetVelocity_FeedbackMessage_feedback
{
public:
  explicit Init_SetVelocity_FeedbackMessage_feedback(::my_robot_interfaces::action::SetVelocity_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::action::SetVelocity_FeedbackMessage feedback(::my_robot_interfaces::action::SetVelocity_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_FeedbackMessage msg_;
};

class Init_SetVelocity_FeedbackMessage_goal_id
{
public:
  Init_SetVelocity_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetVelocity_FeedbackMessage_feedback goal_id(::my_robot_interfaces::action::SetVelocity_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_SetVelocity_FeedbackMessage_feedback(msg_);
  }

private:
  ::my_robot_interfaces::action::SetVelocity_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::action::SetVelocity_FeedbackMessage>()
{
  return my_robot_interfaces::action::builder::Init_SetVelocity_FeedbackMessage_goal_id();
}

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__ACTION__DETAIL__SET_VELOCITY__BUILDER_HPP_
